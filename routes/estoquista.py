from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user

from app import db
from models.item import Item
from models.os import OrdemServico
from models.movimento_estoque import MovimentoEstoque

estoquista_bp = Blueprint('estoquista', __name__, template_folder='templates/estoquista')

def verifica_permissao():
    if current_user.role != 'estoquista':
        flash('Acesso negado.')
        return False
    return True

@estoquista_bp.route('/dashboard')
@login_required
def dashboard():
    if not verifica_permissao():
        return redirect(url_for('auth.login'))
    return render_template('estoquista/dashboard.html')

@estoquista_bp.route('/estoque_disponivel')
@login_required
def estoque_disponivel():
    if not verifica_permissao():
        return redirect(url_for('auth.login'))

    itens = Item.query.order_by(Item.nome.asc()).all()
    return render_template('estoquista/estoque_disponivel.html', itens=itens)

@estoquista_bp.route('/entrada_estoque', methods=['GET', 'POST'])
@login_required
def entrada_estoque():
    if not verifica_permissao():
        return redirect(url_for('auth.login'))

    itens = Item.query.order_by(Item.nome.asc()).all()

    if request.method == 'POST':
        item_id = request.form.get('item_id')
        quantidade = request.form.get('quantidade')

        if not item_id or not quantidade:
            flash('Por favor, preencha todos os campos.')
            return redirect(url_for('estoquista.entrada_estoque'))

        try:
            item = Item.query.get(int(item_id))
            qtd = int(quantidade)

            if qtd <= 0:
                flash('Quantidade deve ser maior que zero.')
                return redirect(url_for('estoquista.entrada_estoque'))

            item.quantidade += qtd

            movimento = MovimentoEstoque(
                item_id=item.id,
                tipo='entrada',
                quantidade=qtd,
                usuario_id=current_user.id,
                observacao='Entrada manual de estoque (reposição)'
            )
            db.session.add(movimento)
            db.session.commit()

            flash(f'{qtd} unidade(s) adicionadas ao estoque de {item.nome}.')
            return redirect(url_for('estoquista.estoque_disponivel'))

        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao adicionar estoque: {str(e)}')
            return redirect(url_for('estoquista.entrada_estoque'))

    return render_template('estoquista/entrada_estoque.html', itens=itens)

@estoquista_bp.route('/movimentacoes', methods=['GET', 'POST'])
@login_required
def movimentacoes():
    if not verifica_permissao():
        return redirect(url_for('auth.login'))

    pendentes = OrdemServico.query.filter_by(status='pendente').all()

    if request.method == 'POST':
        try:
            for item in pendentes:
                acao = request.form.get(f'acao_{item.id}')
                if acao == 'aprovar':
                    if item.item.quantidade < item.quantidade:
                        flash(f'Estoque insuficiente para o item {item.item.nome}.')
                        continue

                    item.status = 'aprovado'
                    item.item.quantidade -= item.quantidade

                    movimento = MovimentoEstoque(
                        item_id=item.item.id,
                        tipo='saida',
                        quantidade=item.quantidade,
                        usuario_id=current_user.id,
                        observacao=f'Aprovado para O.S. {item.ordem_servico_id}'
                    )
                    db.session.add(movimento)

                elif acao == 'reprovar':
                    item.status = 'reprovado'

            db.session.commit()
            flash('Itens atualizados com sucesso.')

        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar itens: {str(e)}')

        return redirect(url_for('estoquista.movimentacoes'))

    return render_template('estoquista/movimentacoes.html', pendentes=pendentes)

@estoquista_bp.route('/cadastrar-item', methods=['GET', 'POST'])
@login_required
def cadastrar_item():
    if current_user.role != 'estoquista':
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form.get('descricao')
        quantidade = int(request.form['quantidade'])

        novo_item = Item(nome=nome, descricao=descricao, quantidade=quantidade)
        db.session.add(novo_item)
        db.session.commit()
        flash('Item cadastrado com sucesso!', 'success')
        return redirect(url_for('estoquista.dashboard'))

    return render_template('estoquista/novo_item.html')