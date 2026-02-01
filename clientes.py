"""
clientes.py

Happy Burger - Avance 2
Este módulo define la clase Cliente y su administrador.
El manejo de datos se realiza únicamente en memoria.
"""

class Cliente:
    """
    Representa un cliente del sistema.

    Atributos:
        id_cliente (int): Identificador del cliente.
        nombre (str): Nombre del cliente.
        telefono (str): Teléfono del cliente.
    """

    def __init__(self, id_cliente, nombre, telefono):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.telefono = telefono

    def to_dict(self):
        """Convierte el cliente a diccionario."""
        return {
            "id_cliente": self.id_cliente,
            "nombre": self.nombre,
            "telefono": self.telefono
        }

    def actualizar(self, nombre=None, telefono=None):
        """Actualiza los datos del cliente."""
        if nombre:
            self.nombre = nombre
        if telefono:
            self.telefono = telefono


class ClientesManager:
    """
    Administra clientes en memoria.
    """

    def __init__(self):
        self._clientes = {}
        self._contador_id = 1

    def listar(self):
        """Lista todos los clientes."""
        return [c.to_dict() for c in self._clientes.values()]

    def agregar(self, nombre, telefono):
        """Agrega un cliente."""
        cliente = Cliente(self._contador_id, nombre, telefono)
        self._clientes[self._contador_id] = cliente
        self._contador_id += 1
        return cliente.to_dict()

    def eliminar(self, id_cliente):
        """Elimina un cliente por ID."""
        if id_cliente in self._clientes:
            del self._clientes[id_cliente]
            return True
        return False

    def actualizar(self, id_cliente, nombre=None, telefono=None):
        """Actualiza un cliente."""
        if id_cliente not in self._clientes:
            return False
        self._clientes[id_cliente].actualizar(nombre, telefono)
        return True

    def buscar_por_id(self, id_cliente):
        """Busca un cliente por ID."""
        cliente = self._clientes.get(id_cliente)
        return cliente.to_dict() if cliente else None
