"""
pedidos.py

Happy Burger - Avance 3
- Crea pedidos consultando cliente y productos (menu)
- Guarda pedido y sus items en SQLite
- Genera un ticket .txt por pedido
"""

from datetime import datetime
from pathlib import Path

from db import get_connection


class Pedido:
    """Representa un pedido y permite calcular totales."""

    def __init__(self, id_pedido, id_cliente, fecha):
        self.id_pedido = id_pedido
        self.id_cliente = id_cliente
        self.fecha = fecha
        self.items = []

    def agregar_item(self, id_item, nombre, precio, unidades):
        self.items.append({
            "id_item": int(id_item),
            "nombre": str(nombre),
            "precio": float(precio),
            "unidades": int(unidades),
        })

    def calcular_subtotal(self):
        return sum(i["precio"] * i["unidades"] for i in self.items)

    def calcular_total(self, tasa_iva=0.16):
        subtotal = self.calcular_subtotal()
        iva = subtotal * tasa_iva
        total = subtotal + iva
        return subtotal, iva, total


class PedidosManager:
    """Administra pedidos usando SQLite."""

    def crear_pedido(self, id_cliente, items, tasa_iva=0.16):
        """
        Crea un pedido en la BD con sus items y genera ticket.

        Args:
            id_cliente (int): ID del cliente.
            items (list[dict]): items con id_item, nombre, precio, unidades
            tasa_iva (float): IVA simulado.

        Returns:
            int: id_pedido creado.
        """
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        pedido = Pedido(id_pedido=None, id_cliente=int(id_cliente), fecha=fecha)
        for it in items:
            pedido.agregar_item(it["id_item"], it["nombre"], it["precio"], it["unidades"])

        subtotal, iva, total = pedido.calcular_total(tasa_iva=tasa_iva)

        conn = get_connection()
        cur = conn.cursor()

        # Insert pedido
        cur.execute(
            """
            INSERT INTO pedidos (id_cliente, fecha, subtotal, iva, total)
            VALUES (?, ?, ?, ?, ?);
            """,
            (pedido.id_cliente, pedido.fecha, subtotal, iva, total)
        )
        id_pedido = cur.lastrowid

        # Insert items
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
        conn.close()

        # Generar ticket
        self.generar_ticket_txt(id_pedido)

        return id_pedido

    def obtener_pedido(self, id_pedido):
        """
        Obtiene un pedido y sus items desde la BD.

        Returns:
            dict | None: {"pedido": {...}, "items": [...]}
        """
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM pedidos WHERE id_pedido = ?;",
            (int(id_pedido),)
        )
        pedido = cur.fetchone()
        if not pedido:
            conn.close()
            return None

        cur.execute(
            "SELECT * FROM pedido_items WHERE id_pedido = ? ORDER BY id_pedido_item;",
            (int(id_pedido),)
        )
        items = cur.fetchall()
        conn.close()

        return {
            "pedido": dict(pedido),
            "items": [dict(i) for i in items]
        }

    def generar_ticket_txt(self, id_pedido):
        """
        Genera un archivo .txt con el ticket del pedido.
        """
        data = self.obtener_pedido(id_pedido)
        if not data:
            return False

        pedido = data["pedido"]
        items = data["items"]

        Path("tickets").mkdir(exist_ok=True)

        ruta = Path("tickets") / f"ticket_{id_pedido}.txt"

        lineas = []
        lineas.append("====================================")
        lineas.append("            HAPPY BURGER            ")
        lineas.append("              TICKET                ")
        lineas.append("====================================")
        lineas.append(f"Pedido #: {pedido['id_pedido']}")
        lineas.append(f"Cliente: {pedido['id_cliente']}")
        lineas.append(f"Fecha  : {pedido['fecha']}")
        lineas.append("------------------------------------")

        for it in items:
            lineas.append(
                f"{it['unidades']} x {it['nombre']} @ ${it['precio']:.2f} = ${it['total_linea']:.2f}"
            )

        lineas.append("------------------------------------")
        lineas.append(f"Subtotal: ${pedido['subtotal']:.2f}")
        lineas.append(f"IVA     : ${pedido['iva']:.2f}")
        lineas.append(f"TOTAL   : ${pedido['total']:.2f}")
        lineas.append("====================================")

        ruta.write_text("\n".join(lineas), encoding="utf-8")
        return True
