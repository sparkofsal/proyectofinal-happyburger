"""
menu.py

Happy Burger - Avance 3
CRUD de productos del menú con SQLite, manteniendo estructura OOP.
"""

from db import get_connection


class MenuItem:
    """Representa un producto del menú."""

    def __init__(self, id_item, nombre, precio):
        self.id_item = id_item
        self.nombre = nombre
        self.precio = float(precio)

    def to_dict(self):
        return {
            "id_item": self.id_item,
            "nombre": self.nombre,
            "precio": self.precio
        }


class MenuManager:
    """Administra productos del menú usando SQLite (CRUD)."""

    def listar(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id_item, nombre, precio FROM menu ORDER BY id_item;")
        filas = cur.fetchall()
        conn.close()
        return [dict(f) for f in filas]

    def agregar(self, nombre, precio):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO menu (nombre, precio) VALUES (?, ?);",
            (nombre.strip(), float(precio))
        )
        conn.commit()
        nuevo_id = cur.lastrowid
        conn.close()
        return self.buscar_por_id(nuevo_id)

    def actualizar(self, id_item, nombre=None, precio=None):
        item = self.buscar_por_id(id_item)
        if not item:
            return False

        nuevo_nombre = nombre.strip() if nombre else item["nombre"]
        nuevo_precio = float(precio) if precio is not None else item["precio"]

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE menu SET nombre = ?, precio = ? WHERE id_item = ?;",
            (nuevo_nombre, nuevo_precio, int(id_item))
        )
        conn.commit()
        conn.close()
        return True

    def eliminar(self, id_item):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM menu WHERE id_item = ?;", (int(id_item),))
        conn.commit()
        filas = cur.rowcount
        conn.close()
        return filas > 0

    def buscar_por_id(self, id_item):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT id_item, nombre, precio FROM menu WHERE id_item = ?;",
            (int(id_item),)
        )
        fila = cur.fetchone()
        conn.close()
        return dict(fila) if fila else None
