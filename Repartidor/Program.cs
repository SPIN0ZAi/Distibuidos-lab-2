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

            var channel = GrpcChannel.ForAddress("http://localhost:5000", new GrpcChannelOptions { HttpHandler = httpHandler });
            var client = new RestauranteService.RestauranteServiceClient(channel);

            Console.WriteLine("Repartidor iniciado. Esperando pedidos para repartir...");

            while (true)
            {
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
    }
}
