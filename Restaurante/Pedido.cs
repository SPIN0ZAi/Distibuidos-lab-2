using System.Collections.Generic;
using Restaurante;

namespace RestauranteApp
{
    public class Pedido
    {
        public int Id { get; set; }
        public List<PlatoPedido> Platos { get; set; } = new List<PlatoPedido>();
        public int Distancia { get; set; }
        public string Estado { get; set; } = "En preparacion";
        public int TiempoEstimado => Distancia * 5;
    }
}
