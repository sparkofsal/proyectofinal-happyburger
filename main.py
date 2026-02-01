"""
main.py

Happy Burger - Avance 3
Consola con persistencia SQLite:
- CRUD Clientes
- CRUD Menú
- Crear pedidos guardando en BD
- Generar ticket .txt por pedido
"""

from db import init_db, asegurar_carpeta_tickets
from clientes import ClientesManager
from menu import MenuManager
from pedidos import PedidosManager


def pausar():
    input("\nPresiona Enter para continuar...")


def leer_entero_positivo(mensaje):
    while True:
        txt = input(mensaje).strip()
        if not txt.isdigit():
            print("❌ Ingresa un número entero válido.")
            continue
        val = int(txt)
        if val < 1:
            print("❌ El número debe ser >= 1.")
            continue
        return val


def leer_float_positivo(mensaje):
    while True:
        txt = input(mensaje).strip()
        try:
            val = float(txt)
        except ValueError:
            print("❌ Ingresa un número válido (ej. 10 o 10.50).")
            continue
        if val <= 0:
            print("❌ El número debe ser mayor que 0.")
            continue
        return val


def menu_principal():
    print("\n==============================")
    print("        HAPPY BURGER          ")
    print("           Avance 3           ")
    print("==============================")
    print("1) Clientes (CRUD)")
    print("2) Menú (CRUD)")
    print("3) Pedidos")
    print("4) Salir")


def sub_menu_clientes(cm: ClientesManager):
    while True:
        print("\n--- CLIENTES (CRUD) ---")
        print("1) Listar")
        print("2) Agregar")
        print("3) Actualizar")
        print("4) Eliminar")
        print("5) Regresar")

        op = input("Opción: ").strip()

        if op == "1":
            clientes = cm.listar()
            if not clientes:
                print("No hay clientes registrados.")
            else:
                for c in clientes:
                    print(f"ID {c['id_cliente']} | {c['nombre']} | {c['telefono']}")
            pausar()

        elif op == "2":
            nombre = input("Nombre: ").strip()
            telefono = input("Teléfono: ").strip()
            if not nombre or not telefono:
                print("❌ Nombre y teléfono son obligatorios.")
                pausar()
                continue
            nuevo = cm.agregar(nombre, telefono)
            print(f"✅ Cliente agregado: ID {nuevo['id_cliente']}")
            pausar()

        elif op == "3":
            idc = leer_entero_positivo("ID cliente a actualizar: ")
            actual = cm.buscar_por_id(idc)
            if not actual:
                print("❌ No existe ese cliente.")
                pausar()
                continue
            nombre = input(f"Nuevo nombre (Enter para '{actual['nombre']}'): ").strip()
            telefono = input(f"Nuevo teléfono (Enter para '{actual['telefono']}'): ").strip()
            nombre = nombre if nombre else None
            telefono = telefono if telefono else None
            cm.actualizar(idc, nombre=nombre, telefono=telefono)
            print("✅ Cliente actualizado.")
            pausar()

        elif op == "4":
            idc = leer_entero_positivo("ID cliente a eliminar: ")
            ok = cm.eliminar(idc)
            print("✅ Cliente eliminado." if ok else "❌ No existe ese cliente.")
            pausar()

        elif op == "5":
            break
        else:
            print("❌ Opción inválida.")
            pausar()


def sub_menu_menu(mm: MenuManager):
    while True:
        print("\n--- MENÚ (CRUD) ---")
        print("1) Listar")
        print("2) Agregar")
        print("3) Actualizar")
        print("4) Eliminar")
        print("5) Regresar")

        op = input("Opción: ").strip()

        if op == "1":
            items = mm.listar()
            if not items:
                print("No hay productos registrados.")
            else:
                for it in items:
                    print(f"ID {it['id_item']} | {it['nombre']} | ${it['precio']:.2f}")
            pausar()

        elif op == "2":
            nombre = input("Nombre del producto: ").strip()
            if not nombre:
                print("❌ El nombre es obligatorio.")
                pausar()
                continue
            precio = leer_float_positivo("Precio: ")
            nuevo = mm.agregar(nombre, precio)
            print(f"✅ Producto agregado: ID {nuevo['id_item']}")
            pausar()

        elif op == "3":
            idi = leer_entero_positivo("ID producto a actualizar: ")
            actual = mm.buscar_por_id(idi)
            if not actual:
                print("❌ No existe ese producto.")
                pausar()
                continue
            nombre = input(f"Nuevo nombre (Enter para '{actual['nombre']}'): ").strip()
            precio_txt = input(f"Nuevo precio (Enter para '{actual['precio']}'): ").strip()

            nombre = nombre if nombre else None
            precio = None
            if precio_txt:
                try:
                    precio = float(precio_txt)
                except ValueError:
                    print("❌ Precio inválido.")
                    pausar()
                    continue

            mm.actualizar(idi, nombre=nombre, precio=precio)
            print("✅ Producto actualizado.")
            pausar()

        elif op == "4":
            idi = leer_entero_positivo("ID producto a eliminar: ")
            ok = mm.eliminar(idi)
            print("✅ Producto eliminado." if ok else "❌ No existe ese producto.")
            pausar()

        elif op == "5":
            break
        else:
            print("❌ Opción inválida.")
            pausar()


def sub_menu_pedidos(cm: ClientesManager, mm: MenuManager, pm: PedidosManager):
    while True:
        print("\n--- PEDIDOS ---")
        print("1) Crear pedido")
        print("2) Consultar pedido por número")
        print("3) Regresar")

        op = input("Opción: ").strip()

        if op == "1":
            # 1) Elegir cliente existente
            id_cliente = leer_entero_positivo("ID del cliente: ")
            cliente = cm.buscar_por_id(id_cliente)
            if not cliente:
                print("❌ Ese cliente no existe. Agrégalo en Clientes.")
                pausar()
                continue

            # 2) Agregar productos existentes
            items_pedido = []
            print("\nAgrega productos al pedido (Enter para terminar).")

            while True:
                productos = mm.listar()
                if not productos:
                    print("❌ No hay productos en el menú. Agrega productos primero.")
                    break

                for p in productos:
                    print(f"ID {p['id_item']} | {p['nombre']} | ${p['precio']:.2f}")

                id_txt = input("\nID producto (Enter para terminar): ").strip()
                if id_txt == "":
                    break
                if not id_txt.isdigit():
                    print("❌ ID inválido.")
                    continue

                id_item = int(id_txt)
                prod = mm.buscar_por_id(id_item)
                if not prod:
                    print("❌ Producto no existe.")
                    continue

                unidades = leer_entero_positivo("Unidades: ")
                items_pedido.append({
                    "id_item": prod["id_item"],
                    "nombre": prod["nombre"],
                    "precio": prod["precio"],
                    "unidades": unidades
                })
                print("✅ Producto agregado.")

            if not items_pedido:
                print("❌ No se creó pedido porque no agregaste productos.")
                pausar()
                continue

            # 3) Guardar pedido + ticket
            id_pedido = pm.crear_pedido(id_cliente, items_pedido)
            print(f"\n✅ Pedido guardado con número: {id_pedido}")
            print(f"✅ Ticket generado: tickets/ticket_{id_pedido}.txt")
            pausar()

        elif op == "2":
            id_pedido = leer_entero_positivo("Número de pedido: ")
            data = pm.obtener_pedido(id_pedido)
            if not data:
                print("❌ No existe ese pedido.")
                pausar()
                continue

            pedido = data["pedido"]
            items = data["items"]

            print("\n==============================")
            print("     PEDIDO ENCONTRADO        ")
            print("==============================")
            print(f"Pedido #: {pedido['id_pedido']}")
            print(f"Cliente: {pedido['id_cliente']}")
            print(f"Fecha  : {pedido['fecha']}")
            print("------------------------------")
            for it in items:
                print(f"{it['unidades']} x {it['nombre']} = ${it['total_linea']:.2f}")
            print("------------------------------")
            print(f"Subtotal: ${pedido['subtotal']:.2f}")
            print(f"IVA     : ${pedido['iva']:.2f}")
            print(f"TOTAL   : ${pedido['total']:.2f}")
            print("==============================")

            pausar()

        elif op == "3":
            break
        else:
            print("❌ Opción inválida.")
            pausar()


def main():
    # Inicialización del sistema (tablas + carpeta tickets)
    init_db()
    asegurar_carpeta_tickets()

    cm = ClientesManager()
    mm = MenuManager()
    pm = PedidosManager()

    while True:
        menu_principal()
        op = input("Selecciona una opción: ").strip()

        if op == "1":
            sub_menu_clientes(cm)
        elif op == "2":
            sub_menu_menu(mm)
        elif op == "3":
            sub_menu_pedidos(cm, mm, pm)
        elif op == "4":
            print("\n✅ Saliendo... ¡Gracias por usar Happy Burger!")
            break
        else:
            print("❌ Opción inválida.")
            pausar()


if __name__ == "__main__":
    main()
