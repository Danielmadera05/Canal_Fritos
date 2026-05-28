from extensions import db

class Cliente(db.Model):
    __tablename__ = "cliente"

    cli_id = db.Column(db.Integer, primary_key=True)
    cli_nombre = db.Column(db.String(100))
    cli_email = db.Column(db.String(100))
    cli_telefono = db.Column(db.String(15))
    cli_foto = db.Column(db.String(500))
    cli_password = db.Column(db.String(255))
    cli_address = db.Column(db.String(200))
