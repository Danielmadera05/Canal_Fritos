from extensions import db
from datetime import datetime, timedelta

class Pedido(db.Model):
    __tablename__ = "pedido"

    ped_id = db.Column(db.Integer, primary_key=True)
    cli_id = db.Column(db.Integer, db.ForeignKey("cliente.cli_id"))
    ped_total = db.Column(db.Float(10,2))
    ped_fecha = db.Column(db.DateTime,default=datetime.utcnow)
    ped_limite_pago = db.Column(db.DateTime)
    ped_metodo_pago = db.Column(db.String(50))
    ped_referencia = db.Column(db.String(100))
    ped_estado = db.Column(db.String(50))
    tie_id = db.Column(db.Integer, db.ForeignKey("tienda.tie_id"))
    cliente = db.relationship("Cliente", backref="pedidos") # Relación con el modelo Cliente
    tienda = db.relationship("Tienda", backref="pedidos") # Relación con el modelo Tienda