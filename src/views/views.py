from flask import (
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from main import app, db
from models.models import Jogos, Usuarios


@app.route('/')
def home():
    game_list = Jogos.query.all()
    return render_template('index.html', title='Jogos', game_list=game_list)


@app.route('/novo-jogo', methods=['GET', 'POST'])
def new_game():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect('/login?next-page=/novo-jogo')
    if request.method == 'POST':
        name = request.form['nome']
        category = request.form['categoria']
        console = request.form['console']
        game_db = Jogos.query.filter_by(nome=name).first()
        if game_db:
            flash('Jogo já cadastrado!')
            return redirect(url_for('new_game'))
        new_game = Jogos(nome=name, categoria=category, console=console)
        db.session.add(new_game)
        db.session.commit()
        flash('Jogo cadastrado com sucesso!')
        return redirect(url_for('home'))
    return render_template('form.html', title='Cadastrar Jogo')


@app.route('/atualizar/<int:game_id>', methods=['GET', 'POST'])
def update_game(game_id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(f'/login?next-page=/atualizar/{game_id}')
    if request.method == 'POST':
        game = Jogos.query.get(game_id)
        game.nome = request.form['nome']
        game.categoria = request.form['categoria']
        game.console = request.form['console']
        db.session.commit()
        db.session.refresh(game)
        flash('Jogo atualizado com sucesso!')
        return redirect(url_for('home'))
    game = Jogos.query.get(game_id)
    return render_template('form.html', title='Atualizar Jogo', game=game)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_db = Usuarios.query.filter_by(
            username=request.form['user']
        ).first()
        if user_db and user_db.senha == request.form['password']:
            session['usuario_logado'] = user_db.username
            flash(user_db.username + ' logado com sucesso!')
            next_page = request.form.get('next-page')
            return redirect(next_page)
        flash('Usuário ou senha inválidos!')
        return redirect(url_for('home'))
    next_page = request.args.get('next-page',)
    return render_template('login.html', title='Login', next_page=next_page)


@app.route('/logout')
def logout():
    session.pop('usuario_logado', None)
    flash('Usuário deslogado com sucesso!')
    return redirect(url_for('login'))
