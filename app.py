from flask import Flask
from config import Config
from extensions import db
# Import blueprints from controllers
from controllers.fritosController import fritos_bp
from controllers.clienteController import auth_bp
from controllers.carritoController import cart_bp
from controllers.pedidoController import pedido_bp
from controllers.tiendaController import tienda_bp
from controllers.adminController import admin_bp   

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
