from extensions import db

class Tienda(db.Model):
    __tablename__="tienda"

    tie_id = db.Column(db.Integer,primary_key=True)
    tie_nombre = db.Column(db.String(100),nullable=False)
    tie_direccion = db.Column(db.String(200))
    tie_imagen = db.Column(db.String(500))