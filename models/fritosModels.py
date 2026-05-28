from extensions import db

#MODELO DE FRITOS
class Fritos(db.Model):
    __tablename__ = "fritos"

    fri_id = db.Column(db.Integer, primary_key=True)
    fri_nombre = db.Column(db.String(100))
    fri_precio = db.Column(db.Float)
    fri_foto = db.Column(db.String(200))
    fri_stock = db.Column(db.Integer)
    tie_id = db.Column(db.Integer,db.ForeignKey("tienda.tie_id")) #RELACION CON TIENDA
    tienda = db.relationship("Tienda", backref="fritos") #RELACION CON TIENDA 