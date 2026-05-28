from extensions import db   

class PedidoDetalle(db.Model):
    __tablename__ = "pedido_detalle"

    det_id = db.Column(db.Integer, primary_key=True)
    ped_id = db.Column(db.Integer, db.ForeignKey("pedido.ped_id"))
    fri_id = db.Column(db.Integer, db.ForeignKey("fritos.fri_id"))
    cantidad = db.Column(db.Integer)
    precio = db.Column(db.Float(10,2)) 
    frito = db.relationship("Fritos", backref="detalles")