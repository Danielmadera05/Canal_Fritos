from flask import Blueprint, render_template, request, redirect, session
from models.clienteModels import Cliente
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash # Para encriptar y verificar contraseñas


auth_bp = Blueprint("auth", __name__)

# REGISTRO
@auth_bp.route("/registro", methods=["GET","POST"])
def register():
    if request.method == "POST":
        nombre = request.form["name"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"]) # Encriptar contraseña
        telefono = request.form["telefono"]
        direccion = request.form["address"]
        foto = request.files.get("cli_foto")  # Obtener foto si se proporciona

        print("Foto recibida en el registro:", foto)    
        
        # Si se proporciona una foto, guardarla en la carpeta estática 
        if foto:
            foto.save(f"static/uploads/{foto.filename}")
            nombre_foto = foto.filename
        else:
            nombre_foto = None


        cliente = Cliente(
            cli_nombre=nombre,
            cli_email=email,
            cli_password=password,
            cli_telefono=telefono,
            cli_address=direccion,
            cli_foto=nombre_foto # Asignar el nombre de la foto aquí
        )

        db.session.add(cliente)
        db.session.commit()

        return redirect("/login") # Redirigir al login después del registro exitoso

    return render_template("registro.html")

# LOGIN
@auth_bp.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        cliente = Cliente.query.filter_by(cli_email=email).first() # Buscar cliente por email

        if cliente and check_password_hash(cliente.cli_password, password): # Verificar contraseña
            session["cliente_id"] = cliente.cli_id
            session["cliente_nombre"] = cliente.cli_nombre
            session["cliente_foto"] = cliente.cli_foto or "default.png"
            return redirect("/") # Redirigir a la página principal después del login exitoso

    return render_template("login.html")

#PERFIL
@auth_bp.route("/perfil")
def perfil():

    if not session.get("cliente_id"):
        return redirect("/login")

    cliente = Cliente.query.get(session["cliente_id"])

    return render_template("perfil.html", cliente=cliente)


#EDITAR PERFIL
@auth_bp.route("/perfil/editar", methods=["GET","POST"])
def editar_perfil():

    # Verificar si el cliente está logueado
    if not session.get("cliente_id"):
        return redirect("/login")

    # Obtener el cliente desde la base de datos
    cliente = Cliente.query.get(session["cliente_id"])

    if request.method == "POST":

        cliente.cli_nombre = request.form["nombre"]
        cliente.cli_email = request.form["email"]
        cliente.cli_telefono = request.form["telefono"]
        cliente.cli_address = request.form["address"]

        # CAMBIO DE FOTO
        foto = request.files.get("foto")
        if foto and foto.filename != "":
            foto.save(f"static/uploads/{foto.filename}")
            cliente.cli_foto = foto.filename

        # CAMBIO CONTRASEÑA
        nueva_pass = request.form.get("password")
        if nueva_pass != "":
            cliente.cli_password = generate_password_hash(nueva_pass)

        db.session.commit()
        return redirect("/perfil")

    return render_template("editar_perfil.html", cliente=cliente)


# LOGOUT
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")
