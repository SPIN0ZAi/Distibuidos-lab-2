using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Restaurante;
using ClienteApp;

namespace Cliente
{
    class Program
    {
        static async Task Main(string[] args)
        {
            var clientService = new RestauranteClienteService();
            clientService.ConnectAsync();
            Console.WriteLine("Conectado al servidor gRPC.");

            while (true)
            {
                Console.WriteLine("\n=== Menú ===");
                Console.WriteLine("1. Hacer un pedido");
                Console.WriteLine("2. Consultar estado del pedido");
                Console.WriteLine("3. Salir");
                Console.Write("Opcion: ");
                
                var opcion = Console.ReadLine();
                
                // Keep asking for an option if it's invalid, without reprinting the whole menu
                while (string.IsNullOrWhiteSpace(opcion) || (opcion != "1" && opcion != "2" && opcion != "3"))
                {
                    if (!string.IsNullOrWhiteSpace(opcion))
                    {
                        Console.WriteLine("Opción no válida.");
                    }
                    Console.Write("Opcion: ");
                    opcion = Console.ReadLine();
                }

                if (opcion == "1")
                {
                    var platos = new List<PlatoPedido>();
                    while(true)
                    {
                        Console.Write("Nombre del plato (o vacio para terminar): ");
                        var nombre = Console.ReadLine();
                        if (string.IsNullOrWhiteSpace(nombre)) break;

                        Console.Write("Cantidad: ");
                        if (int.TryParse(Console.ReadLine(), out int cantidad))
                        {
                            platos.Add(new PlatoPedido { Nombre = nombre, Cantidad = cantidad });
                        }
                    }

                    if (platos.Count > 0)
                    {
                        Console.Write("Distancia de envio: ");
                        if (int.TryParse(Console.ReadLine(), out int distancia))
                        {
                            try
                            {
                                await clientService.HacerPedidoAsync(platos, distancia);
                            }
                            catch { }
                        }
                    }
                }
                else if (opcion == "2")
                {
                    Console.Write("ID del pedido: ");
                    if (int.TryParse(Console.ReadLine(), out int id))
                    {
                        await clientService.ConsultarEstadoPedidoAsync(id);
                    }
                }
                else if (opcion == "3")
                {
                    break;
                }
            }
        }
    }
}
