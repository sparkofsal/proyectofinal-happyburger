"""
Happy Burger - Avance 1 (MEJORADO)
Aplicación de consola (simulación)

Objetivo del Avance 1:
- Crear un menú base en consola
- Controlar el flujo del programa con funciones, condicionales y bucles
- Simular el cálculo de un pedido (producto, precio, unidades)

MEJORA (sin salir del Avance 1):
- Permite agregar VARIOS productos a un mismo pedido (carrito simulado)
- Genera ticket final con desglose e IVA simulado

IMPORTANTE:
- NO usar clases todavía
- NO usar base de datos
- Todo es simulación en consola
"""


def pausar():
    """Pausa la ejecución para que el usuario pueda leer y continuar."""
    input("\nPresiona Enter para continuar...")


def leer_opcion_menu():
    """
    Muestra el menú principal y devuelve la opción elegida.

    Retorna:
        str: opción ingresada (ej. '1', '2', '3', '4').
    """
    print("\n==============================")
    print("        HAPPY BURGER          ")
    print("==============================")
    print("1) Pedidos")
    print("2) Clientes")
    print("3) Menú")
    print("4) Salir")
    return input("Selecciona una opción (1-4): ").strip()


def leer_entero_positivo(mensaje):
    """
    Pide un entero positivo y valida la entrada.

    Args:
        mensaje (str): texto para solicitar el número.

    Retorna:
        int: entero positivo (>= 1).
    """
    while True:
        texto = input(mensaje).strip()
        if not texto.isdigit():
            print("❌ Error: escribe un número entero válido (por ejemplo 1, 2, 3).")
            continue

        valor = int(texto)
        if valor < 1:
            print("❌ Error: el número debe ser mayor o igual a 1.")
            continue

        return valor


def leer_opcion_si_no(mensaje):
    """
    Pide una respuesta tipo sí/no y valida.

    Args:
        mensaje (str): texto de la pregunta.

    Retorna:
        bool: True si es sí, False si es no.
    """
    while True:
        resp = input(mensaje).strip().lower()
        if resp in ("s", "si", "sí", "y", "yes"):
            return True
        if resp in ("n", "no"):
            return False
        print("❌ Respuesta inválida. Escribe: s/n")


def obtener_productos():
    """
    Define el catálogo simulado de productos.

    Retorna:
        dict: productos disponibles por id.
    """
    return {
        1: {"nombre": "Hamburguesa Clásica", "precio": 89.00},
        2: {"nombre": "Hamburguesa Doble", "precio": 119.00},
        3: {"nombre": "Papas", "precio": 45.00},
        4: {"nombre": "Refresco", "precio": 30.00},
    }


def mostrar_catalogo_productos(productos):
    """
    Muestra el catálogo simulado en consola.

    Args:
        productos (dict): catálogo con ids, nombre y precio.
    """
    print("\n--- Catálogo de productos (simulación) ---")
    for clave, info in productos.items():
        print(f"{clave}) {info['nombre']} - ${info['precio']:.2f}")


def calcular_totales(carrito, tasa_iva=0.16):
    """
    Calcula subtotal, IVA y total a partir del carrito.

    Args:
        carrito (list): lista de ítems (dicts) con precio y cantidad.
        tasa_iva (float): porcentaje de IVA simulado.

    Retorna:
        tuple: (subtotal, iva, total)
    """
    subtotal = 0.0
    for item in carrito:
        subtotal += item["precio_unitario"] * item["unidades"]

    iva = subtotal * tasa_iva
    total = subtotal + iva
    return subtotal, iva, total


def imprimir_ticket(carrito, subtotal, iva, total):
    """
    Imprime el ticket final con desglose del carrito.

    Args:
        carrito (list): ítems del pedido.
        subtotal (float): subtotal calculado.
        iva (float): iva calculado.
        total (float): total calculado.
    """
    print("\n==============================")
    print("        TICKET (SIM)          ")
    print("==============================")

    if not carrito:
        print("No hay productos en el pedido.")
        print("==============================")
        return

    for idx, item in enumerate(carrito, start=1):
        nombre = item["nombre"]
        unidades = item["unidades"]
        precio = item["precio_unitario"]
        linea_total = precio * unidades
        print(f"{idx}. {nombre}")
        print(f"   {unidades} x ${precio:.2f} = ${linea_total:.2f}")

    print("------------------------------")
    print(f"Subtotal : ${subtotal:.2f}")
    print(f"IVA 16%  : ${iva:.2f}")
    print(f"TOTAL    : ${total:.2f}")
    print("==============================")


def simular_pedido():
    """
    Simula la creación de un pedido con múltiples productos:
    - Muestra catálogo
    - Permite agregar productos al carrito
    - Calcula totales
    - Imprime ticket final

    Todo es simulación y no se guarda nada.
    """
    productos = obtener_productos()
    carrito = []

    print("\n📦 PEDIDOS (Avance 1 - Simulación)")
    print("Vas a armar un pedido agregando productos al carrito.\n")

    while True:
        mostrar_catalogo_productos(productos)

        opcion_producto = leer_entero_positivo("\nElige el número de producto: ")
        if opcion_producto not in productos:
            print("❌ Producto no válido. Intenta de nuevo.")
            continue

        unidades = leer_entero_positivo("¿Cuántas unidades? ")

        seleccionado = productos[opcion_producto]
        carrito.append(
            {
                "id_producto": opcion_producto,
                "nombre": seleccionado["nombre"],
                "precio_unitario": seleccionado["precio"],
                "unidades": unidades,
            }
        )

        print(f"✅ Agregado: {unidades} x {seleccionado['nombre']}")

        seguir = leer_opcion_si_no("\n¿Quieres agregar otro producto? (s/n): ")
        if not seguir:
            break

    subtotal, iva, total = calcular_totales(carrito)
    imprimir_ticket(carrito, subtotal, iva, total)


def opcion_pedidos():
    """Opción 1 del menú: Pedidos. En Avance 1 solo se simula el cálculo."""
    simular_pedido()
    pausar()


def opcion_clientes():
    """Opción 2 del menú: Clientes. En Avance 1 solo es un placeholder."""
    print("\n👤 CLIENTES (Avance 1 - Simulación)")
    print("Aquí más adelante podremos agregar / eliminar / actualizar clientes.")
    print("Por ahora, solo estamos creando el menú y el flujo del programa.")
    pausar()


def opcion_menu():
    """Opción 3 del menú: Menú. En Avance 1 solo se muestra el catálogo."""
    print("\n🍔 MENÚ (Avance 1 - Simulación)")
    productos = obtener_productos()
    mostrar_catalogo_productos(productos)
    pausar()


def main():
    """Controla el flujo del programa con un bucle y condicionales."""
    while True:
        opcion = leer_opcion_menu()

        if opcion == "1":
            opcion_pedidos()
        elif opcion == "2":
            opcion_clientes()
        elif opcion == "3":
            opcion_menu()
        elif opcion == "4":
            print("\n✅ Saliendo... ¡Gracias por usar Happy Burger!")
            break
        else:
            print("\n❌ Opción inválida. Elige una opción del 1 al 4.")
            pausar()


if __name__ == "__main__":
    main()
