from app import db

class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=0)
    descricao = db.Column(db.String(255))

    def __repr__(self):
        return f'<Item {self.nome}>'