using System;
using System.Net.Http;
using System.Threading.Tasks;
using Grpc.Net.Client;
using Google.Protobuf.WellKnownTypes;
using Restaurante;
using Grpc.Core;

namespace RepartidorApp
{
    class Program
    {
        static async Task Main(string[] args)
        {
            var httpHandler = new HttpClientHandler
            {
                ServerCertificateCustomValidationCallback = HttpClientHandler.DangerousAcceptAnyServerCertificateValidator
            };

            var channel = GrpcChannel.ForAddress("http://172.20.10.9:5000", new GrpcChannelOptions { HttpHandler = httpHandler });
            var client = new RestauranteService.RestauranteServiceClient(channel);

            Console.WriteLine("Repartidor iniciado. Esperando pedidos para repartir...");
            Console.WriteLine("Cliente gRPC del Repartidor");
            Console.WriteLine("1. Tomar pedido para repartir");
            Console.WriteLine("2. Salir");

            while (true)
            {
                Console.Write("\nElige una opción (1-2): ");
                var opcion = Console.ReadLine();

                switch (opcion)
                {
                    case "1":
                        await TomarPedidoParaRepartir(client);
                        break;
                    case "2":
                        return;
                    default:
                        Console.WriteLine("Opción no válida");
                        break;
                }
                try
                {
                    var response = await client.TomarPedidoParaRepartirAsync(new Empty());
                    Console.WriteLine($"[Asignado] {response.Mensaje} (ID: {response.IdPedido})");
                    
                    Console.WriteLine("Entregando...");
                    await Task.Delay(3000); // Simulate delivery time
                    Console.WriteLine($"[Entregado] Pedido ID: {response.IdPedido} entregado con exito.\n");
                }
                catch (RpcException ex)
                {
                    Console.WriteLine($"[Error] {ex.Status.Detail}");
                    await Task.Delay(2000); // Retry delay
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"[Excepcion] No se pudo conectar: {ex.Message}");
                    await Task.Delay(3000); // Retry delay
                }
            }
        }

        static async Task TomarPedidoParaRepartir(RestauranteService.RestauranteServiceClient client)
        {
            try
                {
                    var response = await client.TomarPedidoParaRepartirAsync(new Empty());
                    Console.WriteLine($"ID del pedido recibido: {response.IdPedido}");
                    Console.WriteLine($"Distancia al destino: {response.Distancia} km"); 
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"ERROR HAPPENED");
                }

        }

    }
}
