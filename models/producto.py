from models import db


class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, default=1)
    medida = db.Column(db.String(20), nullable=False)
    comprado = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Producto {self.nombre}>'
