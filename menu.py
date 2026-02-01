"""
menu.py

Happy Burger - Avance 2
Este módulo define los productos del menú y su administración.
Los datos se manejan únicamente en memoria.
"""

class MenuItem:
    """
    Representa un producto del menú.
    """

    def __init__(self, id_item, nombre, precio):
        self.id_item = id_item
        self.nombre = nombre
        self.precio = float(precio)

    def to_dict(self):
        """Convierte el producto a diccionario."""
        return {
            "id_item": self.id_item,
            "nombre": self.nombre,
            "precio": self.precio
        }

    def actualizar(self, nombre=None, precio=None):
        """Actualiza los datos del producto."""
        if nombre:
            self.nombre = nombre
        if precio is not None:
            self.precio = float(precio)


class MenuManager:
    """
    Administra productos del menú en memoria.
    """

    def __init__(self):
        self._items = {}
        self._contador_id = 1

        self.agregar("Hamburguesa Clásica", 89)
        self.agregar("Hamburguesa Doble", 119)
        self.agregar("Papas", 45)
        self.agregar("Refresco", 30)

    def listar(self):
        """Lista todos los productos."""
        return [i.to_dict() for i in self._items.values()]

    def agregar(self, nombre, precio):
        """Agrega un producto."""
        item = MenuItem(self._contador_id, nombre, precio)
        self._items[self._contador_id] = item
        self._contador_id += 1
        return item.to_dict()

    def eliminar(self, id_item):
        """Elimina un producto."""
        if id_item in self._items:
            del self._items[id_item]
            return True
        return False

    def actualizar(self, id_item, nombre=None, precio=None):
        """Actualiza un producto."""
        if id_item not in self._items:
            return False
        self._items[id_item].actualizar(nombre, precio)
        return True

    def buscar_por_id(self, id_item):
        """Busca un producto por ID."""
        item = self._items.get(id_item)
        return item.to_dict() if item else None
