using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Server.Kestrel.Core;
using Microsoft.Extensions.DependencyInjection;
using System;
using RestauranteApp;

var builder = WebApplication.CreateBuilder(args);

// Configurar Kestrel para permitir HTTP/2 sin TLS
builder.WebHost.ConfigureKestrel(options =>
{
    // Configurar el servidor para escuchar en HTTP/2 sin TLS en el puerto 5000
    options.ListenLocalhost(5000, o => o.Protocols = HttpProtocols.Http2); // http2 es el protocolo gRPC
});

// Agregar servicios gRPC
builder.Services.AddGrpc();

// Registrar RestauranteService como Singleton para mantener el estado
builder.Services.AddSingleton<RestauranteService>(); // addSingleton crea una instancia del servicio que se comparte entre todas las peticiones

var app = builder.Build();

// Registra el servicio gRPC para que pueda recibir y gestionar invocaciones remotas.
app.MapGrpcService<RestauranteService>();

// Configurar una página de inicio simple
app.MapGet("/", () => "Servidor gRPC del Restaurante ejecutándose...");

Console.WriteLine("Iniciando servidor gRPC del Restaurante...");
Console.WriteLine("Presiona Ctrl+C para salir");

app.Run();
