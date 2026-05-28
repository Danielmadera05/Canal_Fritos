from flask import Flask
from config import Config
from extensions import db
from flask import make_response, request # Importar make_response y request para manejar respuestas y solicitudes HTTP
# Import blueprints from controllers
from controllers.fritosController import fritos_bp
from controllers.clienteController import auth_bp
from controllers.carritoController import cart_bp
from controllers.pedidoController import pedido_bp
from controllers.tiendaController import tienda_bp
from controllers.adminController import admin_bp 
# Import PyMySQL for MySQL database connection 
import pymysql
import os
from dotenv import load_dotenv

load_dotenv() 

# Establacer la conexión a la base de datos utilizando PyMySQL y las variables de entorno
conexion = pymysql.connect(
    host=os.getenv("MYSQL_HOST"),
    port=int(os.getenv("MYSQL_PORT")),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DB"),
    cursorclass=pymysql.cursors.DictCursor
)

try:
    print("Conexión exitosa 🚀")
except Exception as e:
    print("Error al conectar a la base de datos:")
    print("Error:", e)


# Initialize Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Register blueprints for different controllers
app.register_blueprint(fritos_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(tienda_bp)
app.register_blueprint(pedido_bp)
app.register_blueprint(admin_bp)

# Set a secret key for session management
app.secret_key = "clave_super_secreta"

# Run the application
if __name__ == "__main__":
    app.run(debug=True)
