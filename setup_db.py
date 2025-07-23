from app import create_app, db
from models.usuario import Usuario

app = create_app()

with app.app_context():
    # Cria as tabelas do banco
    db.drop_all()   # Opcional: apaga tudo antes de criar (se quiser resetar)
    db.create_all()

    # Usuários iniciais
    usuarios = [
        Usuario(username='operador1', senha='1234', role='operador'),
        Usuario(username='estoquista1', senha='1234', role='estoquista'),
        Usuario(username='tecnico1', senha='1234', role='tecnico'),
    ]

    # Adiciona e salva no banco
    db.session.add_all(usuarios)
    db.session.commit()

    print('Banco criado e usuários iniciais adicionados com sucesso!')
