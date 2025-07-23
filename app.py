from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'supersecreto'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///controle_estoque.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    

    from routes.auth import auth_bp
    app.register_blueprint(auth_bp)
    from routes.operador import operador_bp
    app.register_blueprint(operador_bp, url_prefix='/operador')
    from routes.estoquista import estoquista_bp
    app.register_blueprint(estoquista_bp, url_prefix='/estoquista')
    # ...registrar outros blueprints

    return app
