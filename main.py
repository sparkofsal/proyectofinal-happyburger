"""
main.py

Happy Burger - Avance 2
Aplicación de consola estructurada con Programación Orientada a Objetos.
"""

from clientes import ClientesManager
from menu import MenuManager
from pedidos import PedidosManager


def pausar():
    input("\nPresiona Enter para continuar...")


def leer_entero(mensaje):
    while True:
        valor = input(mensaje).strip()
        if valor.isdigit():
            return int(valor)
        print("❌ Ingresa un número válido.")


def menu_principal():
    print("\n==============================")
    print("        HAPPY BURGER          ")
    print("           Avance 2           ")
    print("==============================")
    print("1) Pedidos")
    print("2) Clientes")
    print("3) Menú")
    print("4) Salir")


def main():
    clientes = ClientesManager()
    menu = MenuManager()
    pedidos = PedidosManager()

    while True:
        menu_principal()
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            print("\nPEDIDOS (simulación)")
            pausar()

        elif opcion == "2":
            print("\nCLIENTES (simulación)")
            for c in clientes.listar():
                print(c)
            pausar()

        elif opcion == "3":
            print("\nMENÚ (simulación)")
            for p in menu.listar():
                print(p)
            pausar()

        elif opcion == "4":
            print("\nSaliendo del sistema...")
            break

        else:
            print("❌ Opción inválida.")
            pausar()


if __name__ == "__main__":
    main()
