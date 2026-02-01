"""
clientes.py

Happy Burger - Avance 3
CRUD de clientes con SQLite, manteniendo estructura OOP.
"""

from db import get_connection


class Cliente:
    """Representa un cliente del sistema."""

    def __init__(self, id_cliente, nombre, telefono):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.telefono = telefono

    def to_dict(self):
        return {
            "id_cliente": self.id_cliente,
            "nombre": self.nombre,
            "telefono": self.telefono
        }


class ClientesManager:
    """Administra clientes usando SQLite (CRUD)."""

    def listar(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id_cliente, nombre, telefono FROM clientes ORDER BY id_cliente;")
        filas = cur.fetchall()
        conn.close()
        return [dict(f) for f in filas]

    def agregar(self, nombre, telefono):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO clientes (nombre, telefono) VALUES (?, ?);",
            (nombre.strip(), telefono.strip())
        )
        conn.commit()
        nuevo_id = cur.lastrowid
        conn.close()
        return self.buscar_por_id(nuevo_id)

    def actualizar(self, id_cliente, nombre=None, telefono=None):
        cliente = self.buscar_por_id(id_cliente)
        if not cliente:
            return False

        nuevo_nombre = nombre.strip() if nombre else cliente["nombre"]
        nuevo_telefono = telefono.strip() if telefono else cliente["telefono"]

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE clientes SET nombre = ?, telefono = ? WHERE id_cliente = ?;",
            (nuevo_nombre, nuevo_telefono, int(id_cliente))
        )
        conn.commit()
        conn.close()
        return True

    def eliminar(self, id_cliente):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM clientes WHERE id_cliente = ?;", (int(id_cliente),))
        conn.commit()
        filas = cur.rowcount
        conn.close()
        return filas > 0

    def buscar_por_id(self, id_cliente):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT id_cliente, nombre, telefono FROM clientes WHERE id_cliente = ?;",
            (int(id_cliente),)
        )
        fila = cur.fetchone()
        conn.close()
        return dict(fila) if fila else None
