from app import db
from datetime import datetime

class OrdemServico(db.Model):
    __tablename__ = 'ordens_servico'
    id = db.Column(db.Integer, primary_key=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(30), default='AGUARDANDO CONFIRMAÇÃO DO ESTOQUE')
    descricao = db.Column(db.Text, nullable=False)
    local_servico = db.Column(db.String(150), nullable=False)
    central_cliente = db.Column(db.String(150), nullable=False)
    nome_cliente = db.Column(db.String(150), nullable=False)

    operador_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    tecnico_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    estoquista_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)

    data_finalizacao = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<O.S. {self.id} - {self.status}>'