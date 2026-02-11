"""
pedidos.py

Gestión de pedidos:
- Guarda pedidos e items en SQLite
- Calcula totales
- Genera un ticket .txt por pedido
"""

from datetime import datetime
from pathlib import Path

from db import get_connection

TICKETS_DIR = Path("tickets")


class Pedido:
    """Representa un pedido y permite calcular totales."""

    def __init__(self, id_pedido, id_cliente, fecha):
        self.id_pedido = id_pedido
        self.id_cliente = id_cliente
        self.fecha = fecha
        self.items = []

    def agregar_item(self, id_item, nombre, precio, unidades):
        """Agrega un producto al pedido (en memoria)."""
        self.items.append({
            "id_item": int(id_item),
            "nombre": str(nombre),
            "precio": float(precio),
            "unidades": int(unidades),
        })

    def calcular_subtotal(self):
        """Suma el total de todas las líneas del pedido."""
        return sum(i["precio"] * i["unidades"] for i in self.items)

    def calcular_total(self, tasa_iva=0.16):
        """Calcula subtotal, IVA y total."""
        subtotal = self.calcular_subtotal()
        iva = subtotal * tasa_iva
        total = subtotal + iva
        return subtotal, iva, total


class PedidosManager:
    """
    Maneja operaciones de pedidos en la base de datos.
    Esta clase es usada desde main.py y desde app.py (consulta web).
    """

    def crear_pedido(self, id_cliente, items, tasa_iva=0.16):
        """
        Crea un pedido con sus items, lo guarda en SQLite y genera su ticket.

        Args:
            id_cliente (int): ID del cliente.
            items (list[dict]): lista con {id_item, nombre, precio, unidades}.
            tasa_iva (float): IVA simulado.

        Returns:
            int: número de pedido creado.
        """
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        pedido = Pedido(id_pedido=None, id_cliente=int(id_cliente), fecha=fecha)
        for it in items:
            pedido.agregar_item(it["id_item"], it["nombre"], it["precio"], it["unidades"])

        subtotal, iva, total = pedido.calcular_total(tasa_iva=tasa_iva)

        with get_connection() as conn:
            cur = conn.cursor()

            cur.execute(
                """
                INSERT INTO pedidos (id_cliente, fecha, subtotal, iva, total)
                VALUES (?, ?, ?, ?, ?);
                """,
                (pedido.id_cliente, pedido.fecha, subtotal, iva, total)
            )
            id_pedido = cur.lastrowid

            for it in pedido.items:
                total_linea = it["precio"] * it["unidades"]
                cur.execute(
                    """
                    INSERT INTO pedido_items (id_pedido, id_item, nombre, precio, unidades, total_linea)
                    VALUES (?, ?, ?, ?, ?, ?);
                    """,
                    (id_pedido, it["id_item"], it["nombre"], it["precio"], it["unidades"], total_linea)
                )

            conn.commit()

        self.generar_ticket_txt(id_pedido)
        return id_pedido

    def obtener_pedido(self, id_pedido):
        """
        Obtiene un pedido y sus items desde SQLite.

        Returns:
            dict | None: {"pedido": {...}, "items": [...]}
        """
        with get_connection() as conn:
            cur = conn.cursor()

            cur.execute("SELECT * FROM pedidos WHERE id_pedido = ?;", (int(id_pedido),))
            pedido = cur.fetchone()
            if not pedido:
                return None

            cur.execute(
                "SELECT * FROM pedido_items WHERE id_pedido = ? ORDER BY id_pedido_item;",
                (int(id_pedido),)
            )
            items = cur.fetchall()

        return {
            "pedido": dict(pedido),
            "items": [dict(i) for i in items]
        }

    def generar_ticket_txt(self, id_pedido):
        """Genera el archivo .txt del ticket para un pedido."""
        data = self.obtener_pedido(id_pedido)
        if not data:
            return False

        pedido = data["pedido"]
        items = data["items"]

        TICKETS_DIR.mkdir(exist_ok=True)
        ruta = TICKETS_DIR / f"ticket_{id_pedido}.txt"

        lineas = [
            "====================================",
            "            HAPPY BURGER            ",
            "              TICKET                ",
            "====================================",
            f"Pedido #: {pedido['id_pedido']}",
            f"Cliente: {pedido['id_cliente']}",
            f"Fecha  : {pedido['fecha']}",
            "------------------------------------",
        ]

        for it in items:
            lineas.append(
                f"{it['unidades']} x {it['nombre']} @ ${it['precio']:.2f} = ${it['total_linea']:.2f}"
            )

        lineas.extend([
            "------------------------------------",
            f"Subtotal: ${pedido['subtotal']:.2f}",
            f"IVA     : ${pedido['iva']:.2f}",
            f"TOTAL   : ${pedido['total']:.2f}",
            "====================================",
        ])

        ruta.write_text("\n".join(lineas), encoding="utf-8")
        return True
