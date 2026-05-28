from flask import Blueprint, render_template, session, redirect
from extensions import db
from models.pedidoModels import Pedido
from models.fritosModels import Fritos
from models.detalleModels import PedidoDetalle

pedido_bp = Blueprint("pedido", __name__)

# Ruta para ver las compras realizadas por el cliente
@pedido_bp.route("/mis-compras")
def mis_compras():

    if not session.get("cliente_id"):
        return redirect("/login")

    pedidos = Pedido.query.filter_by(
        cli_id=session["cliente_id"]
    ).all()

    return render_template("mis_compras.html",pedidos=pedidos)

# Ruta para ver el detalle de una compra específica
@pedido_bp.route("/detalle-compra/<int:ped_id>")
def detalle_compra(ped_id):

    if not session.get("cliente_id"):
        return redirect("/login")

    detalles = db.session.query(PedidoDetalle,Fritos
                                ).join(Fritos, PedidoDetalle.fri_id == Fritos.fri_id
                                       ).filter(PedidoDetalle.ped_id == ped_id
                                                ).all()

    return render_template("detalle_pedido.html",detalles=detalles)