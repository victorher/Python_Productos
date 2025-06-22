from models import db
from flask_login import UserMixin

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    usuario = db.Column(db.String(80), unique=True, nullable=False)
    clave = db.Column(db.String(200), nullable=False)
    estado = db.Column(db.Boolean, default=True)
    es_admin = db.Column(db.Boolean, default=False)

def __repr__(self):
    return f'<Usuario {self.usuario}>'
    
@property
def is_active(self):
    return self.estado
