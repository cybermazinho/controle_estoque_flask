from app import db
from flask_login import UserMixin

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    senha = db.Column(db.String(120), nullable=False)  # Pra simplificar, sem hash aqui (melhorar depois)
    role = db.Column(db.String(20), nullable=False)  # 'operador', 'estoquista', 'tecnico'

    def __repr__(self):
        return f'<Usuario {self.username} - {self.role}>'
