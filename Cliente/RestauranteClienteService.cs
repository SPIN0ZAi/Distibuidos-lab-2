using Grpc.Net.Client;
using Grpc.Core;
using System;
using System.Threading.Tasks;
using System.Collections.Generic;
using Restaurante;

namespace ClienteApp
{
    public class RestauranteClienteService
    {
        private GrpcChannel? _channel;
        private RestauranteService.RestauranteServiceClient? _client;

        public void ConnectAsync()
        {
            AppContext.SetSwitch("System.Net.Http.SocketsHttpHandler.Http2UnencryptedSupport", true);
            
            _channel = GrpcChannel.ForAddress("http://localhost:5000");
            _client = new RestauranteService.RestauranteServiceClient(_channel);
        }

        public async Task HacerPedidoAsync(List<PlatoPedido> platos, int distancia)
        {
            var request = new PedidoRequest { Distancia = distancia };
            request.Platos.AddRange(platos);

            try
            {
                var response = await _client!.HacerPedidoAsync(request);
                Console.WriteLine($"[Exito] Pedido ID: {response.IdPedido} - {response.Mensaje}");
            }
            catch (RpcException ex)
            {
                Console.WriteLine($"[Error] Code: {ex.StatusCode}, Mensaje: {ex.Status.Detail}");
                throw;
            }
        }

        public async Task ConsultarEstadoPedidoAsync(int idPedido)
        {
            var request = new ConsultaRequest { IdPedido = idPedido };
            
            try
            {
                var response = await _client!.ConsultarEstadoPedidoAsync(request);
                Console.WriteLine($"[Estado] {response.Estado}");
                Console.WriteLine($"[Mensaje] {response.Mensaje}");
                Console.WriteLine($"[Tiempo Estimado] {response.TiempoEstimado} mins");
            }
            catch (RpcException ex)
            {
                Console.WriteLine($"[Error] No se pudo consultar: {ex.Status.Detail}");
            }
        }
    }
}
