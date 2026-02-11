"""
clientes.py

Gestión de clientes del sistema.
Este módulo maneja las operaciones CRUD de clientes usando SQLite.
"""

from db import get_connection


class Cliente:
    """Representa un cliente."""

    def __init__(self, id_cliente, nombre, telefono):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.telefono = telefono

    def to_dict(self):
        """Convierte el cliente a diccionario para uso interno."""
        return {
            "id_cliente": self.id_cliente,
            "nombre": self.nombre,
            "telefono": self.telefono
        }


class ClientesManager:
    """
    Maneja las operaciones de clientes en la base de datos.
    Esta clase es usada directamente desde main.py.
    """

    def listar(self):
        """Obtiene todos los clientes registrados."""
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT id_cliente, nombre, telefono "
                "FROM clientes ORDER BY id_cliente;"
            )
            return [dict(f) for f in cur.fetchall()]

    def agregar(self, nombre, telefono):
        """Agrega un cliente nuevo y devuelve el registro creado."""
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO clientes (nombre, telefono) VALUES (?, ?);",
                (nombre.strip(), telefono.strip())
            )
            conn.commit()
            nuevo_id = cur.lastrowid

        return self.buscar_por_id(nuevo_id)

    def actualizar(self, id_cliente, nombre=None, telefono=None):
        """Actualiza los datos de un cliente existente."""
        cliente = self.buscar_por_id(id_cliente)
        if not cliente:
            return False

        nuevo_nombre = nombre.strip() if nombre else cliente["nombre"]
        nuevo_telefono = telefono.strip() if telefono else cliente["telefono"]

        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "UPDATE clientes SET nombre = ?, telefono = ? WHERE id_cliente = ?;",
                (nuevo_nombre, nuevo_telefono, int(id_cliente))
            )
            conn.commit()

        return True

    def eliminar(self, id_cliente):
        """Elimina un cliente por ID."""
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "DELETE FROM clientes WHERE id_cliente = ?;",
                (int(id_cliente),)
            )
            conn.commit()
            return cur.rowcount > 0

    def buscar_por_id(self, id_cliente):
        """Busca un cliente por su ID."""
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT id_cliente, nombre, telefono "
                "FROM clientes WHERE id_cliente = ?;",
                (int(id_cliente),)
            )
            fila = cur.fetchone()

        return dict(fila) if fila else None
