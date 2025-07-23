from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from models.os import OrdemServico
from datetime import datetime

operador_bp = Blueprint('operador', __name__, template_folder='templates/operador')

# Dashboard com lista de O.S. do operador
@operador_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'operador':
        flash('Acesso negado')
        return redirect(url_for('auth.login'))
    
    ordens = OrdemServico.query.filter_by(operador_id=current_user.id).order_by(OrdemServico.data_criacao.desc()).all()
    return render_template('operador/dashboard.html', ordens=ordens)

# Tela para criar nova O.S.
@operador_bp.route('/nova_os', methods=['GET', 'POST'])
@login_required
def nova_os():
    if current_user.role != 'operador':
        flash('Acesso negado')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        descricao = request.form.get('descricao')
        local_servico = request.form.get('local_servico')
        central_cliente = request.form.get('central_cliente')
        nome_cliente = request.form.get('nome_cliente')

        if not descricao or not local_servico or not central_cliente or not nome_cliente:
            flash('Preencha todos os campos')
            return redirect(url_for('operador.nova_os'))

        nova_os = OrdemServico(
            descricao=descricao,
            local_servico=local_servico,
            central_cliente=central_cliente,
            nome_cliente=nome_cliente,
            operador_id=current_user.id,
            status='AGUARDANDO CONFIRMAÇÃO DO ESTOQUE'
        )
        db.session.add(nova_os)
        db.session.commit()
        flash('Ordem de Serviço criada com sucesso!')
        return redirect(url_for('operador.dashboard'))

    return render_template('operador/nova_os.html')
