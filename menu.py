"""
menu.py

Gestión de productos del menú.
Este módulo maneja las operaciones CRUD del menú usando SQLite.
"""

from db import get_connection


class MenuItem:
    """Representa un producto del menú."""

    def __init__(self, id_item, nombre, precio):
        self.id_item = id_item
        self.nombre = nombre
        self.precio = float(precio)

    def to_dict(self):
        """Convierte el producto a diccionario para uso interno."""
        return {
            "id_item": self.id_item,
            "nombre": self.nombre,
            "precio": self.precio
        }


class MenuManager:
    """
    Maneja las operaciones de productos del menú en la base de datos.
    Esta clase es usada directamente desde main.py.
    """

    def listar(self):
        """Obtiene todos los productos registrados."""
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT id_item, nombre, precio "
                "FROM menu ORDER BY id_item;"
            )
            return [dict(f) for f in cur.fetchall()]

    def agregar(self, nombre, precio):
        """Agrega un producto nuevo y devuelve el registro creado."""
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO menu (nombre, precio) VALUES (?, ?);",
                (nombre.strip(), float(precio))
            )
            conn.commit()
            nuevo_id = cur.lastrowid

        return self.buscar_por_id(nuevo_id)

    def actualizar(self, id_item, nombre=None, precio=None):
        """Actualiza un producto existente."""
        item = self.buscar_por_id(id_item)
        if not item:
            return False

        nuevo_nombre = nombre.strip() if nombre else item["nombre"]
        nuevo_precio = float(precio) if precio is not None else item["precio"]

        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "UPDATE menu SET nombre = ?, precio = ? WHERE id_item = ?;",
                (nuevo_nombre, nuevo_precio, int(id_item))
            )
            conn.commit()

        return True

    def eliminar(self, id_item):
        """Elimina un producto por ID."""
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "DELETE FROM menu WHERE id_item = ?;",
                (int(id_item),)
            )
            conn.commit()
            return cur.rowcount > 0

    def buscar_por_id(self, id_item):
        """Busca un producto por su ID."""
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT id_item, nombre, precio "
                "FROM menu WHERE id_item = ?;",
                (int(id_item),)
            )
            fila = cur.fetchone()

        return dict(fila) if fila else None
