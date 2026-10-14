# Guía de Ejecución - Sistema de Restaurante Distribuido con gRPC

Este proyecto simula un sistema de gestión de pedidos con tres roles principales: Restaurante, Repartidor y Cliente.

## Instrucciones para ejecutar el código

Para que el sistema funcione correctamente, debes ejecutar los tres proyectos simultáneamente en tres ventanas de terminal independientes. Todos los comandos deben ejecutarse desde la carpeta raíz de la práctica.

### PASO 1: Iniciar el Servidor (Restaurante)
Abre la primera terminal y ejecuta el siguiente comando para iniciar el servidor gRPC:
    dotnet run --project Restaurante

(Deberías ver el mensaje: "Iniciando servidor gRPC del Restaurante...")

### PASO 2: Iniciar el Repartidor
Abre una segunda terminal y ejecuta el siguiente comando:
    dotnet run --project Repartidor

(Deberías ver el mensaje: "Repartidor iniciado. Esperando pedidos para repartir...")

### PASO 3: Iniciar el Cliente
Abre una tercera terminal y ejecuta el siguiente comando:
    dotnet run --project Cliente

(Verás el menú interactivo para hacer pedidos)

## Cómo interactuar con el sistema:
1. Desde el terminal del Cliente, selecciona la opción "1" e introduce los platos que deseas (nombre y cantidad). Para dejar de añadir platos, presiona Enter cuando te pida el nombre.
2. Introduce la distancia de envío. El sistema te devolverá el ID de tu pedido.
3. El servidor registrará el pedido y podrás ver cómo el terminal del Repartidor lo recoge automáticamente y lo marca como "En reparto".
4. Usa la opción "2" en el terminal del Cliente e introduce el ID de tu pedido para comprobar su estado en tiempo real.

Nota: Si al intentar arrancar el Restaurante recibes un error que dice "address already in use" o "Failed to bind to address", significa que el servidor ya se está ejecutando en otra pestaña de tu terminal. Asegúrate de detenerlo (usando Ctrl+C) antes de volver a lanzarlo.
