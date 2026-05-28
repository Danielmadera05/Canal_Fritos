from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, session, redirect, flash
from models.fritosModels import Fritos
from models.pedidoModels import Pedido
from models.detalleModels import PedidoDetalle
from extensions import db

cart_bp = Blueprint("carrito", __name__)

#Add product to cart 
@cart_bp.route("/add-cart/<int:id>", methods=["POST"])
def add_cart(id):

    # 🔒 Validar sesión
    if not session.get("cliente_id"):
        flash("Debes iniciar sesión para agregar productos al carrito", "warning")
        return redirect("/login")

    producto = Fritos.query.get(id)

    # Validar que todos los productos sean de la misma tienda
    if "cart" in session and len(session["cart"]) > 0:

        primer_id = next(iter(session["cart"]))# Obtener el primer producto del carrito para comparar la tienda

        producto_carrito = Fritos.query.get(
            int(primer_id)
        )

        # Si el producto que se intenta agregar no pertenece a la misma tienda que los productos del carrito, mostrar un mensaje de error y redirigir al usuario
        if producto.tie_id != producto_carrito.tie_id:

            flash("Tu carrito contiene productos de otra tienda","warning")
            return redirect(request.referrer)

    # Verificar si el carrito ya existe en la sesión
    if "cart" not in session:
        session["cart"] = {}

    cart = session["cart"]

    # Agregar o actualizar el producto en el carrito
    if str(id) in cart:
        cart[str(id)]["cantidad"] += 1
    else:
        cart[str(id)] = {
            "nombre": producto.fri_nombre,
            "precio": producto.fri_precio,
            "cantidad": 1,
            "tienda_id": producto.tie_id,
            "tienda_nombre": producto.tienda.tie_nombre
        }

    session["cart"] = cart
    flash("Producto agregado al carrito 🛒", "success") # Notificacion por mensaje
    return redirect("/")

#View cart
@cart_bp.route("/cart")
def cart():

        if "cliente_id" not in session:

            flash("Debe iniciar sesión","warning")
            return redirect("/login")

        carrito = session.get("cart", {})
        return render_template("carrito.html", carrito=carrito)

#Remove product from cart
@cart_bp.route("/remove_from_cart/<int:producto_id>")
def remove_from_cart(producto_id):
    if "cart" in session:
        session["cart"].pop(str(producto_id), None)
        session.modified = True
    return redirect("/cart")

# Increase product quantity in cart
@cart_bp.route("/increase/<int:producto_id>")
def increase(producto_id):
    if "cart" in session:
        if str(producto_id) in session["cart"]:
            session["cart"][str(producto_id)]["cantidad"] += 1
            session.modified = True
    return redirect("/cart")

# Decrease product quantity in cart
@cart_bp.route("/decrease/<int:producto_id>")
def decrease(producto_id):
    if "cart" in session:
        if str(producto_id) in session["cart"]:
            if session["cart"][str(producto_id)]["cantidad"] > 1:
                session["cart"][str(producto_id)]["cantidad"] -= 1
            else:
                session["cart"].pop(str(producto_id), None)
            session.modified = True
    return redirect("/cart")

# Ruta para finalizar la compra
@cart_bp.route("/checkout")
def checkout():

    # Si el cliente no ha iniciado sesión, redirigir al login
    if "cliente_id" not in session:
        return redirect("/login")

    # Si el carrito está vacío, redirigir al carrito
    if "cart" not in session or len(session["cart"]) == 0:
        return redirect("/cart")

    total = 0

    for item in session["cart"].values():
        total += item["precio"] * item["cantidad"]

    # Crear el pedido
    primer_producto = list(session["cart"].values())[0]

    pedido = Pedido(
        ped_total=total,
        cli_id=session["cliente_id"],
        tie_id=primer_producto["tienda_id"],
        ped_estado="Esperando pago",
        ped_limite_pago=datetime.now() + timedelta(minutes=15)
    )

    db.session.add(pedido)
    db.session.commit()

    # Crear detalles del pedido
    for id, item in session["cart"].items():
        detalle = PedidoDetalle(
            ped_id=pedido.ped_id,
            fri_id=id,
            cantidad=item["cantidad"],
            precio=item["precio"]
        )
        db.session.add(detalle)

    db.session.commit()

    return redirect(f"/pagar/{pedido.ped_id}")

@cart_bp.route("/pagar/<int:id>")
def pagar(id):

    if "cliente_id" not in session:
        return redirect("/login")

    pedido = Pedido.query.get_or_404(id)

    # Validar que el pedido pertenezca al cliente actual
    if pedido.cli_id != session["cliente_id"]:

        flash("No tiene permiso para acceder a este pedido","danger")
        return redirect("/mis-compras")
    
    if pedido.ped_estado == "Pagado":
        flash("Este pedido ya fue pagado","info")
        return redirect("/mis-compras")

    if pedido.ped_estado == "Cancelado":
        flash("Este pedido fue cancelado por exceder limite de tiempo (15 minutos)","warning")
        return redirect("/mis-compras")

    if (pedido.ped_estado=="Esperando pago" and pedido.ped_limite_pago < datetime.now()):

        pedido.ped_estado="Cancelado"
        db.session.commit()

        flash("El tiempo para realizar el pago expiró","danger")
        return redirect("/mis-compras")

    return render_template("pago.html", pedido=pedido)

@cart_bp.route("/politica-reembolso")
def politica_reembolso():
    return render_template("politica_reembolso.html")

@cart_bp.route("/procesar_pago/<int:id>", methods=["POST"])
def procesar_pago(id):

    pedido = Pedido.query.get_or_404(id)

    if pedido.cli_id != session["cliente_id"]:

        flash("Acceso denegado","danger")
        return redirect("/mis-compras")    
    
    if pedido.ped_estado != "Esperando pago":

        flash("El pedido ya no admite pagos","warning")
        return redirect("/mis-compras")

    pedido.ped_estado="Pagado"
    pedido.ped_metodo_pago=request.form["metodo"]

    db.session.commit()
    session.pop("cart",None)

    flash("Pago realizado correctamente","success")
    return redirect("/mis-compras")