from extensions import db

class Administrador(db.Model):

    __tablename__="administrador"

    adm_id=db.Column(db.Integer,primary_key=True)
    adm_nombre=db.Column(db.String(100),nullable=False)
    adm_email=db.Column(db.String(100),nullable=False)
    adm_password=db.Column(db.String(100),nullable=False)
    adm_foto=db.Column(db.String(500),nullable=True)