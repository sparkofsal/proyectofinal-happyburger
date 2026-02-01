"""
app.py

Happy Burger - Avance 4
Aplicación web (Flask) para consultar pedidos por número.
Lee información desde SQLite (happy_burger.db).
"""

from flask import Flask, render_template, request
from pedidos import PedidosManager

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    """
    Página principal:
    - Formulario para buscar pedido por número
    - Muestra resultados si se envía un id_pedido válido
    """
    pedido_id = request.args.get("pedido_id", "").strip()

    resultado = None
    error = None

    if pedido_id != "":
        if not pedido_id.isdigit():
            error = "El número de pedido debe ser un entero (ej. 1, 2, 3)."
        else:
            pm = PedidosManager()
            data = pm.obtener_pedido(int(pedido_id))
            if not data:
                error = f"No se encontró el pedido #{pedido_id}."
            else:
                resultado = data

    return render_template(
        "pedidos.html",
        pedido_id=pedido_id,
        resultado=resultado,
        error=error
    )


if __name__ == "__main__":
    # Ejecutar en modo desarrollo
    app.run(debug=True)
