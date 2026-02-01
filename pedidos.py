"""
pedidos.py

Happy Burger - Avance 2
Este módulo define la estructura de un pedido.
Los pedidos se manejan únicamente en memoria.
"""

class Pedido:
    """
    Representa un pedido del sistema.
    """

    def __init__(self, id_pedido, id_cliente):
        self.id_pedido = id_pedido
        self.id_cliente = id_cliente
        self.items = []

    def agregar_item(self, id_item, nombre, precio, unidades):
        """Agrega un producto al pedido."""
        self.items.append({
            "id_item": id_item,
            "nombre": nombre,
            "precio": float(precio),
            "unidades": int(unidades)
        })

    def calcular_subtotal(self):
        """Calcula el subtotal del pedido."""
        return sum(i["precio"] * i["unidades"] for i in self.items)

    def calcular_total(self, iva=0.16):
        """Calcula subtotal, IVA y total."""
        subtotal = self.calcular_subtotal()
        impuesto = subtotal * iva
        total = subtotal + impuesto
        return subtotal, impuesto, total

    def to_dict(self):
        """Convierte el pedido a diccionario."""
        return {
            "id_pedido": self.id_pedido,
            "id_cliente": self.id_cliente,
            "items": self.items
        }


class PedidosManager:
    """
    Administra pedidos en memoria.
    """

    def __init__(self):
        self._pedidos = {}
        self._contador_id = 1

    def crear_pedido(self, id_cliente):
        """Crea un pedido."""
        pedido = Pedido(self._contador_id, id_cliente)
        self._pedidos[self._contador_id] = pedido
        self._contador_id += 1
        return pedido

    def listar(self):
        """Lista pedidos."""
        return [p.to_dict() for p in self._pedidos.values()]

    def buscar_por_id(self, id_pedido):
        """Busca un pedido por ID."""
        return self._pedidos.get(id_pedido)

    def eliminar(self, id_pedido):
        """Elimina un pedido."""
        if id_pedido in self._pedidos:
            del self._pedidos[id_pedido]
            return True
        return False
