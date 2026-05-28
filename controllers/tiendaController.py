from flask import Blueprint, render_template
from models.tiendaModels import Tienda
from models.fritosModels import Fritos

tienda_bp = Blueprint("tienda", __name__)

@tienda_bp.route("/")
def listar_tiendas():

    tiendas = Tienda.query.all()

    return render_template("tiendas.html",tiendas=tiendas)

@tienda_bp.route("/tienda/<int:id>")
def productos_tienda(id):

    tienda = Tienda.query.get_or_404(id) # Verificar que la tienda existe

    productos = Fritos.query.filter_by(tie_id=id).all()

    return render_template("index.html",fritos=productos,tienda=tienda)