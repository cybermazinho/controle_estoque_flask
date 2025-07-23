from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user

from app import db
from models.item import Item
from models.os import OrdemServico
from models.movimento_estoque import MovimentoEstoque

estoquista_bp = Blueprint('estoquista', __name__, url_prefix='/estoquista')


# ---------------- Dashboard Estoquista ----------------
@estoquista_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'estoquista':
        return redirect(url_for('auth.logout'))

    ordens_pendentes = OrdemServico.query.filter_by(status='AGUARDANDO CONFIRMAÇÃO DO ESTOQUE').all()
    return render_template('estoquista/dashboard.html', ordens=ordens_pendentes)


# ---------------- Ver Estoque Disponível ----------------
@estoquista_bp.route('/estoque')
@login_required
def estoque_disponivel():
    if current_user.role != 'estoquista':
        return redirect(url_for('auth.logout'))

    itens = Item.query.all()
    return render_template('estoquista/estoque.html', itens=itens)


# ---------------- Cadastrar Novo Item ----------------
@estoquista_bp.route('/cadastrar-item', methods=['GET', 'POST'])
@login_required
def cadastrar_item():
    if current_user.role != 'estoquista':
        return redirect(url_for('auth.logout'))

    if request.method == 'POST':
        nome = request.form['nome']
        quantidade = int(request.form['quantidade'])
        novo_item = Item(nome=nome, quantidade=quantidade)
        db.session.add(novo_item)
        db.session.commit()
        flash('Item cadastrado com sucesso!', 'success')
        return redirect(url_for('estoquista.estoque_disponivel'))

    return render_template('estoquista/cadastrar_item.html')


# ---------------- Atualizar Item Existente ----------------
@estoquista_bp.route('/entrada', methods=['GET', 'POST'])
@login_required
def entrada_estoque():
    if current_user.role != 'estoquista':
        return redirect(url_for('auth.logout'))

    itens = Item.query.all()

    if request.method == 'POST':
        item_id = int(request.form['item_id'])
        quantidade = int(request.form['quantidade'])

        item = Item.query.get(item_id)
        item.quantidade += quantidade

        mov = MovimentoEstoque(item_id=item.id, tipo='Entrada', quantidade=quantidade, responsavel_id=current_user.id)
        db.session.add(mov)
        db.session.commit()

        flash('Item atualizado com sucesso!', 'success')
        return redirect(url_for('estoquista.estoque_disponivel'))

    return render_template('estoquista/entrada.html', itens=itens)


# ---------------- Histórico de Movimentações ----------------
@estoquista_bp.route('/movimentacoes')
@login_required
def movimentacoes():
    if current_user.role != 'estoquista':
        return redirect(url_for('auth.logout'))

    historico = MovimentoEstoque.query.order_by(MovimentoEstoque.data.desc()).all()
    return render_template('estoquista/movimentacoes.html', historico=historico)


# ---------------- Aprovar/Rejeitar Ordem de Serviço ----------------
@estoquista_bp.route('/aprovar/<int:os_id>', methods=['GET', 'POST'])
@login_required
def aprovar_os(os_id):
    if current_user.role != 'estoquista':
        return redirect(url_for('auth.logout'))

    ordem = OrdemServico.query.get_or_404(os_id)
    print("*" * 50)
    print(ordem)
    print("*" * 50)

    if request.method == 'POST':
        acao = request.form['acao']

        if acao == 'aprovar':
            ordem.status = 'PODE SER INICIADA'
            ordem.estoquista_id = current_user.id

            # registrar saída dos itens no estoque
            for item_os in ordem.itens:
                item_estoque = Item.query.get(item_os.item_id)
                item_estoque.quantidade -= item_os.quantidade

                mov = MovimentoEstoque(
                    item_id=item_estoque.id,
                    tipo='Saída',
                    quantidade=item_os.quantidade,
                    responsavel_id=current_user.id
                )
                db.session.add(mov)

            flash('Ordem de Serviço aprovada e itens liberados.', 'success')

        elif acao == 'rejeitar':
            ordem.status = 'REJEITADA'
            ordem.estoquista_id = current_user.id
            flash('Ordem de Serviço rejeitada.', 'warning')

        db.session.commit()
        return redirect(url_for('estoquista.dashboard'))

    return render_template('estoquista/aprovar_os.html', ordem=ordem)
