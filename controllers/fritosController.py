from flask import Blueprint, render_template
from models.fritosModels import Fritos

fritos_bp = Blueprint("fritos", __name__)

# Route for displaying all products
@fritos_bp.route("/productos")
def index():
    fritos = Fritos.query.all()
    return render_template("index.html", fritos=fritos)