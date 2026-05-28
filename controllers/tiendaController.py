from flask import Blueprint, render_template, request
from models.tiendaModels import Tienda
from models.fritosModels import Fritos

tienda_bp = Blueprint("tienda", __name__)

@tienda_bp.route("/")
def listar_tiendas():

    tiendas = Tienda.query.all()
    cookies = request.cookies.get("cookies")

    return render_template("tiendas.html",tiendas=tiendas, cookies=cookies)

from flask import make_response, redirect

# ACEPTAR COOKIES
@tienda_bp.route("/aceptar_cookies")
def aceptar_cookies():

    respuesta = make_response(redirect("/"))
    respuesta.set_cookie(
        "cookies",
        "aceptadas",
        max_age=60*60*24*365,
        secure=True,
        httponly=True,
        samesite="Lax"
    )

    return respuesta


# RECHAZAR COOKIES
@tienda_bp.route("/rechazar_cookies")
def rechazar_cookies():

    respuesta = make_response(redirect("/"))
    respuesta.set_cookie(
        "cookies",
        "rechazadas",
        max_age=60*60*24*365,
        secure=True,
        httponly=True,
        samesite="Lax"
    )

    return respuesta

@tienda_bp.route("/politica_cookies")
def politica_cookies():
    return render_template("politicas_cookies.html")

@tienda_bp.route("/tienda/<int:id>")
def productos_tienda(id):

    tienda = Tienda.query.get_or_404(id) # Verificar que la tienda existe

    productos = Fritos.query.filter_by(tie_id=id).all()

    return render_template("index.html",fritos=productos,tienda=tienda)