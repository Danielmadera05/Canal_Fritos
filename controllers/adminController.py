from flask import Blueprint, render_template, request, redirect, session, flash
from models.adminModels import Administrador
from models.fritosModels import Fritos
from models.tiendaModels import Tienda
from models.pedidoModels import Pedido
from models.clienteModels import Cliente
from models.detalleModels import PedidoDetalle
from werkzeug.utils import secure_filename
import os
from extensions import db
from sqlalchemy import desc, func

admin_bp=Blueprint("admin",__name__)

# Rutas para el panel de administración
@admin_bp.route("/admin/dashboard")
def admin_dashboard():

    # Verificar si el administrador ha iniciado sesión
    if "admin_id" not in session:
        return redirect("/admin/login")

    # Obtener estadísticas para el dashboard
    total_tiendas = Tienda.query.count()
    total_productos = Fritos.query.count()
    total_pedidos = Pedido.query.count()
    total_clientes = Cliente.query.count()
    ingresos = db.session.query(func.sum(Pedido.ped_total)).scalar() or 0
    pedidos_pendientes = Pedido.query.filter(Pedido.ped_estado=="Solicitado").count()
    ultimos_pedidos = Pedido.query.order_by(Pedido.ped_id.desc()).limit(5).all()
    # Obtener el producto más vendido
    producto_top = db.session.query(Fritos.fri_nombre,func.count(PedidoDetalle.fri_id).label("ventas")
        ).join(PedidoDetalle,Fritos.fri_id == PedidoDetalle.fri_id).group_by(
        Fritos.fri_nombre).order_by(desc("ventas")).first()
    # Obtener ventas por tienda para el gráfico de barras
    ventas_dashboard = db.session.query(Tienda.tie_nombre,func.count(Pedido.ped_id)).join(
        Pedido,Tienda.tie_id == Pedido.tie_id).group_by(Tienda.tie_nombre).all()

    labels_dashboard = []

    datos_dashboard = []

    for tienda, cantidad in ventas_dashboard:

        labels_dashboard.append(tienda)
        datos_dashboard.append(cantidad)

    tienda_lider = db.session.query(Tienda.tie_nombre,func.count(Pedido.ped_id).label("ventas")
        ).join(Pedido,Tienda.tie_id == Pedido.tie_id).group_by(Tienda.tie_nombre).order_by(
        desc("ventas")).first()

    return render_template("admin/dashboard.html",
        total_tiendas=total_tiendas,
        total_productos=total_productos,
        total_pedidos=total_pedidos,
        total_clientes=total_clientes,
        ingresos=ingresos,
        pedidos_pendientes=pedidos_pendientes,
        ultimos_pedidos=ultimos_pedidos,
        producto_top=producto_top,
        labels_dashboard=labels_dashboard,
        datos_dashboard=datos_dashboard,
        tienda_lider=tienda_lider
    )

# Rutas para el inicio de sesión del administrador
@admin_bp.route("/admin/login", methods=["GET","POST"])
def login_admin(): 
    
    if request.method=="POST":

        email=request.form["email"]
        password=request.form["password"]

        # Buscar al administrador en la base de datos
        admin=Administrador.query.filter_by(adm_email=email).first()

        if admin and admin.adm_password==password:
            session["admin_id"]=admin.adm_id
            session["admin_nombre"]=admin.adm_nombre
            session["admin_foto"]=admin.adm_foto

            return redirect("/admin/dashboard")

        flash("Credenciales incorrectas","danger")

    return render_template("admin/login.html")

# Ruta para cerrar sesión del administrador
@admin_bp.route("/admin/logout")
def logout_admin():

    session.pop("admin_id", None)
    session.pop("admin_nombre", None)

    return redirect("/admin/login")

# RUTAS PARA LA GESTIÓN DE TIENDAS
@admin_bp.route("/admin/tiendas")
def listar_tiendas():

    if "admin_id" not in session:
        return redirect("/admin/login")

    tiendas = Tienda.query.all()

    return render_template("admin/tiendas.html", tiendas=tiendas)

# Ruta para crear una nueva tienda
@admin_bp.route("/admin/tiendas/nueva", methods=["GET", "POST"])
def nueva_tienda():

    if "admin_id" not in session:
        return redirect("/admin/login")

    if request.method == "POST":

        nombre = request.form["nombre"]
        direccion = request.form["direccion"]
        imagen = request.files["imagen"]

        nombre_imagen = secure_filename(imagen.filename)

        ruta = os.path.join("static/uploads",nombre_imagen)
        imagen.save(ruta)

        tienda = Tienda(tie_nombre=nombre, tie_direccion=direccion, tie_imagen=nombre_imagen)

        db.session.add(tienda)
        db.session.commit()

        flash("Tienda creada correctamente", "success")
        return redirect("/admin/tiendas")

    return render_template("admin/nueva_tienda.html")

# Ruta para editar una tienda
@admin_bp.route("/admin/tiendas/editar/<int:id>", methods=["GET", "POST"])
def editar_tienda(id):

    if "admin_id" not in session:
        return redirect("/admin/login")

    tienda = Tienda.query.get_or_404(id)

    if request.method == "POST":
        tienda.tie_nombre = request.form["nombre"]
        tienda.tie_direccion = request.form["direccion"]
        imagen = request.files["imagen"]

        if imagen and imagen.filename != "":

            nombre_imagen = secure_filename(imagen.filename)
            ruta = os.path.join("static/uploads",nombre_imagen)

            imagen.save(ruta)

            tienda.tie_imagen = nombre_imagen

        db.session.commit()

        flash("Tienda actualizada correctamente","success")
        return redirect("/admin/tiendas")

    return render_template("admin/editar_tienda.html",tienda=tienda)

# Ruta para eliminar una tienda
@admin_bp.route("/admin/tiendas/eliminar/<int:id>", methods=["GET", "POST"])
def eliminar_tienda(id):

    if "admin_id" not in session:
        return redirect("/admin/login")

    tienda = Tienda.query.get_or_404(id)

    productos = Fritos.query.filter_by(tie_id=id).count()

    if productos > 0:
        flash("No se puede eliminar la tienda porque tiene productos asociados", "danger")
        return redirect("/admin/tiendas")

    db.session.delete(tienda)
    db.session.commit()

    flash("Tienda eliminada correctamente","success")
    return redirect("/admin/tiendas")

# RUTAS PARA LA GESTIÓN DE PRODUCTOS 
@admin_bp.route("/admin/productos")
def listar_productos():

    if "admin_id" not in session:
        return redirect("/admin/login")

    productos = Fritos.query.all()

    return render_template("admin/productos.html", productos=productos)

# Rutas para crear productos
@admin_bp.route("/admin/productos/nuevo", methods=["GET", "POST"])
def nuevo_producto():

    if "admin_id" not in session:
        return redirect("/admin/login")

    tiendas = Tienda.query.all()

    if request.method == "POST":

        nombre = request.form["nombre"]
        precio = request.form["precio"]
        tienda_id = request.form["tienda"]
        imagen = request.files["imagen"]

        nombre_imagen = secure_filename(imagen.filename)

        ruta = os.path.join("static/uploads", nombre_imagen)
        imagen.save(ruta)

        producto = Fritos(fri_nombre=nombre, fri_precio=precio, fri_foto=nombre_imagen, tie_id=tienda_id, fri_stock=10)

        db.session.add(producto) 
        db.session.commit()

        flash("Producto creado correctamente", "success")
        return redirect("/admin/productos")

    return render_template(
        "admin/nuevo_producto.html",
        tiendas=tiendas
    )

# Rutas para editar productos
@admin_bp.route("/admin/productos/editar/<int:id>", methods=["GET", "POST"])
def editar_producto(id):

    if "admin_id" not in session:
        return redirect("/admin/login")

    producto = Fritos.query.get_or_404(id)
    tiendas = Tienda.query.all()

    if request.method == "POST":

        producto.fri_nombre = request.form["nombre"]
        producto.fri_precio = request.form["precio"]
        producto.tie_id = request.form["tienda"]
        imagen = request.files["imagen"]

        if imagen and imagen.filename != "":

            nombre_imagen = secure_filename(imagen.filename)
            ruta = os.path.join("static/uploads", nombre_imagen)

            imagen.save(ruta)
            producto.fri_foto = nombre_imagen

        db.session.commit()

        flash("Producto actualizado correctamente", "success")
        return redirect("/admin/productos")

    return render_template("admin/editar_producto.html", producto=producto, tiendas=tiendas)

# Rutas para eliminar productos
@admin_bp.route("/admin/productos/eliminar/<int:id>")
def eliminar_producto(id):

    if "admin_id" not in session:
        return redirect("/admin/login")

    producto = Fritos.query.get_or_404(id)

    db.session.delete(producto)
    db.session.commit()

    flash("Producto eliminado correctamente", "success")
    return redirect("/admin/productos")

# RUTAS PARA LA GESTIÓN DE PEDIDOS
@admin_bp.route("/admin/pedidos")
def listar_pedidos():

    if "admin_id" not in session:
        return redirect("/admin/login")

    tienda_id = request.args.get("tienda")
    tiendas = Tienda.query.all()
    pedidos_query = Pedido.query


    # Filtrar por tienda si se selecciona una
    if tienda_id:
        pedidos_query = pedidos_query.filter(Pedido.tie_id == tienda_id)

    pedidos = pedidos_query.order_by(Pedido.ped_id.desc()).all()

    return render_template("admin/pedidos.html", pedidos=pedidos, tiendas=tiendas, tienda_actual=tienda_id)

# Rutas para ver detalles de un pedido
@admin_bp.route("/admin/pedidos/detalle/<int:id>")
def detalle_pedido_admin(id):

    if "admin_id" not in session:
        return redirect("/admin/login")

    pedido = Pedido.query.get_or_404(id)
    detalles = PedidoDetalle.query.filter_by(ped_id=id).all()

    return render_template("admin/detalle_pedido.html", pedido=pedido, detalles=detalles)

# Rutas para actualizar el estado de un pedido
@admin_bp.route("/admin/pedidos/estado/<int:id>", methods=["POST"])
def actualizar_estado(id):

    if "admin_id" not in session:
        return redirect("/admin/login")

    pedido = Pedido.query.get_or_404(id)
    pedido.ped_estado = request.form["estado"]

    db.session.commit()

    flash("Estado actualizado correctamente", "success")
    return redirect("/admin/pedidos")

# RUTAS PARA LA GESTIÓN DE CLIENTES
@admin_bp.route("/admin/usuarios")
def listar_usuarios():

    if "admin_id" not in session:
        return redirect("/admin/login")

    busqueda = request.args.get("buscar","")
    usuarios = Cliente.query

    # Filtrar por nombre si se ingresa una búsqueda
    if busqueda:
        usuarios = usuarios.filter(
            Cliente.cli_nombre.like(
                f"%{busqueda}%"
            )
        )

    usuarios = usuarios.all()

    return render_template("admin/usuarios.html", usuarios=usuarios, busqueda=busqueda)

# Rutas para ver detalles de un cliente
@admin_bp.route("/admin/usuarios/ver/<int:id>")
def ver_usuario(id):

    if "admin_id" not in session:
        return redirect("/admin/login")

    usuario = Cliente.query.get_or_404(id)
    pedidos = Pedido.query.filter_by(cli_id=id).order_by(Pedido.ped_id.desc()).all()

    return render_template("admin/ver_usuario.html", usuario=usuario, pedidos=pedidos)

# Rutas para eliminar un cliente si no tiene pedidos asociados
@admin_bp.route("/admin/usuarios/eliminar/<int:id>")
def eliminar_usuario(id):

    if "admin_id" not in session:
        return redirect("/admin/login")

    usuario = Cliente.query.get_or_404(id)
    pedidos = Pedido.query.filter_by(cli_id=id).count()

    if pedidos > 0:
        flash("No se puede eliminar el usuario porque tiene pedidos asociados","danger")
        return redirect("/admin/usuarios")

    db.session.delete(usuario)
    db.session.commit()

    flash("Usuario eliminado correctamente","success")
    return redirect("/admin/usuarios")

# RUTAS PARA REPORTES
@admin_bp.route("/admin/reportes")
def reportes():

    if "admin_id" not in session:
        return redirect("/admin/login")

    total_ingresos = db.session.query(func.sum(Pedido.ped_total)).scalar() or 0
    total_pedidos = Pedido.query.count()
    total_usuarios = Cliente.query.count()

    ventas_tiendas = db.session.query(Tienda.tie_nombre,func.count(Pedido.ped_id)).join(
        Pedido,Tienda.tie_id == Pedido.tie_id).group_by(Tienda.tie_nombre).all()
    
    labels = []
    datos = []

    # Preparar datos para el gráfico de ventas por tienda
    for tienda, cantidad in ventas_tiendas:
        labels.append(tienda)
        datos.append(cantidad)

    return render_template("admin/reportes.html",
        total_ingresos=total_ingresos,
        total_pedidos=total_pedidos,
        total_usuarios=total_usuarios,
        ventas_tiendas=ventas_tiendas,
        labels=labels,
        datos=datos
    )