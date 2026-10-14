using Grpc.Core;
using System.Collections.Concurrent;
using System.Threading;
using System.Threading.Tasks;
using System.Linq;
using Google.Protobuf.WellKnownTypes;
using Restaurante;
using Microsoft.Extensions.Logging;

namespace RestauranteApp
{
    public class RestauranteService : Restaurante.RestauranteService.RestauranteServiceBase
    {
        private readonly ILogger<RestauranteService> _logger;
        private readonly ConcurrentQueue<Pedido> _ordersQueue;
        // Añadimos un diccionario para recordar todos los pedidos históricos, 
        // ya que la cola los elimina cuando el repartidor los toma.
        private readonly ConcurrentDictionary<int, Pedido> _allOrders;
        private const int MaxQueueCapacity = 10;
        private readonly SemaphoreSlim _readyOrdersSemaphore;
        private readonly object _takeLock;
        private int _orderID;

        public RestauranteService(ILogger<RestauranteService> logger)
        {
            _logger = logger;
            _ordersQueue = new ConcurrentQueue<Pedido>();
            _allOrders = new ConcurrentDictionary<int, Pedido>();
            _readyOrdersSemaphore = new SemaphoreSlim(0);
            _takeLock = new object();
            _orderID = 1;
        }

        public override async Task<PedidoResponse> HacerPedido(PedidoRequest request, ServerCallContext context)
        {
            lock (_takeLock) // lock the access to the queue to prevent race conditions
            {
                if (_ordersQueue.Count < MaxQueueCapacity) // checks if the queue is full
                {
                    var pedido = new Pedido // creates a new pedido with the given data
                    {
                        Id = _orderID,
                        Distancia = request.Distancia,
                        Platos = request.Platos.ToList(),
                        Estado = "En preparacion" // sets the initial state of the pedido to "En preparacion"
                    };

                    _ordersQueue.Enqueue(pedido); // adds the pedido to the queue
                    _allOrders.TryAdd(pedido.Id, pedido); // adds the pedido to the dictionary
                    
                    _logger.LogInformation($"pedido {pedido.Id}  registrado.");
                    _orderID++;
                    
                    _readyOrdersSemaphore.Release(); // releases the semaphore to indicate that there is a new order

                    return new PedidoResponse {// returns the response to the client
                        IdPedido = pedido.Id,
                        Mensaje = $"Pedido {pedido.Id} recibido correctamente. Tiempo estimado: {pedido.TiempoEstimado} mins"
                    };
                }
            }
            
            throw new RpcException(new Status(StatusCode.Internal, "La cola está llena"));
        }

        public override Task<EstadoResponse> ConsultarEstadoPedido(ConsultaRequest request, ServerCallContext context)
        {
            // Buscamos en el historial global en lugar de la cola,
            // porque si el repartidor lo ha tomado, ya no está en la cola!
            if (_allOrders.TryGetValue(request.IdPedido, out var pedido)) // tries to get the pedido from the dictionary
            {
                return Task.FromResult(new EstadoResponse // returns the response to the client
                {
                    Estado = pedido.Estado,
                    Mensaje = $"Su pedido está {pedido.Estado}",
                    TiempoEstimado = pedido.Distancia * 5 // calculates the estimated time for the delivery
                });
            }
            else
            {
                throw new RpcException(new Status(StatusCode.NotFound, "El pedido no existe")); // throws an exception if the pedido is not found in the dictionary
            }
        }

        public override async Task<PedidoResponse> TomarPedidoParaRepartir(Empty request, ServerCallContext context)
        {
            await _readyOrdersSemaphore.WaitAsync();

            lock (_takeLock)
            {
                if (_ordersQueue.TryDequeue(out var pedido))
                {
                    pedido.Estado = "En reparto";
                    return new PedidoResponse
                    {
                        IdPedido = pedido.Id,
                        Mensaje = "Pedido en reparto"
                    };
                }
            }
            
            throw new RpcException(new Status(StatusCode.NotFound, "No hay pedidos disponibles"));
        }

        public override Task<PedidoResponse> ConsultarPlatosPedido(ConsultaRequest request, ServerCallContext context)
        {
            if (_allOrders.TryGetValue(request.IdPedido, out var pedido))
            {
                var mensaje = string.Join(", ", pedido.Platos.Select(p => $"{p.Cantidad}x {p.Nombre}"));
                return Task.FromResult(new PedidoResponse {
                    IdPedido = pedido.Id,
                    Mensaje = mensaje
                });
            }
            else
            {
                throw new RpcException(new Status(StatusCode.NotFound, "El pedido no existe"));
            }
        }
    }
}
