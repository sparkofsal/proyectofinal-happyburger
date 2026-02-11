"""
db.py

Conexión y configuración de SQLite.
Aquí se inicializan las tablas del sistema y se asegura la carpeta de tickets.
"""

import sqlite3
from pathlib import Path

DB_NAME = "happy_burger.db"


def get_connection():
    """Crea y retorna una conexión a la base de datos SQLite."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Crea las tablas necesarias si no existen."""
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS menu (
            id_item INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            subtotal REAL NOT NULL,
            iva REAL NOT NULL,
            total REAL NOT NULL,
            FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedido_items (
            id_pedido_item INTEGER PRIMARY KEY AUTOINCREMENT,
            id_pedido INTEGER NOT NULL,
            id_item INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            unidades INTEGER NOT NULL,
            total_linea REAL NOT NULL,
            FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido),
            FOREIGN KEY (id_item) REFERENCES menu(id_item)
        );
        """)

        conn.commit()


def asegurar_carpeta_tickets():
    """Crea la carpeta 'tickets' si no existe."""
    Path("tickets").mkdir(exist_ok=True)
