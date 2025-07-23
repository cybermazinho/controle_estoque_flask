from app import db
from datetime import datetime

class MovimentoEstoque(db.Model):
    __tablename__ = 'movimentos_estoque'

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    tipo = db.Column(db.String(10), nullable=False)  # 'entrada' ou 'saida'
    quantidade = db.Column(db.Integer, nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    observacao = db.Column(db.String(255))

    # Relacionamentos para facilitar acesso via ORM
    item = db.relationship('Item', backref=db.backref('movimentos', lazy=True))
    usuario = db.relationship('Usuario')

    def __repr__(self):
        return f'<MovimentoEstoque {self.tipo} - Item {self.item_id} - Quantidade {self.quantidade}>'
    