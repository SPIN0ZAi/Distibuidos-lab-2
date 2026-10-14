// Configurar Kestrel para permitir HTTP/2 sin TLS 
builder.WebHost.ConfigureKestrel(options => 
{ 
// Configurar el servidor para escuchar en HTTP/2 sin TLS en el puerto 5000 
options.ListenLocalhost(5000, o => o.Protocols = HttpProtocols.Http2); 
}); 
// Agregar servicios gRPC 
builder.Services.AddGrpc(); 
// Registrar RestauranteService como Singleton para mantener el estado 
builder.Services.AddSingleton<RestauranteService>();