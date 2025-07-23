from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models.usuario import Usuario
from app import db, login_manager  # importando as instâncias, não o app

auth_bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        senha = request.form.get('senha')
        user = Usuario.query.filter_by(username=username).first()
        if user and user.senha == senha:
            login_user(user)
            if user.role == 'operador':
                return redirect(url_for('operador.dashboard'))
            elif user.role == 'estoquista':
                return redirect(url_for('estoquista.dashboard'))
            elif user.role == 'tecnico':
                return redirect(url_for('tecnico.dashboard'))
        else:
            flash('Usuário ou senha incorretos')
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
