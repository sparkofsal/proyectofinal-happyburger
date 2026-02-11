"""
app.py

Aplicación web (Flask) para consultar pedidos por número.
Este archivo muestra un formulario y consulta datos desde SQLite.
"""

from flask import Flask, render_template, request
from pedidos import PedidosManager

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    """Página principal: buscar pedido por número y mostrar resultado."""
    pedido_id = request.args.get("pedido_id", "").strip()

    resultado = None
    error = None

    if pedido_id:
        if not pedido_id.isdigit():
            error = "El número de pedido debe ser un entero (ej. 1, 2, 3)."
        else:
            data = PedidosManager().obtener_pedido(int(pedido_id))
            if not data:
                error = f"No se encontró el pedido #{pedido_id}."
            else:
                resultado = data

    return render_template("pedidos.html", pedido_id=pedido_id, resultado=resultado, error=error)


if __name__ == "__main__":
    app.run(debug=True)
