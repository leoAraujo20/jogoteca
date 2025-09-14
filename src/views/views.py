import os

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)

from ..extension import bcrypt, db
from ..forms.forms import FormGame, FormUser
from ..helpers.helpers import remove_image, return_image
from ..models.models import Jogos, Usuarios

bp = Blueprint('views', __name__)


@bp.route('/')
def home():
    game_list = Jogos.query.order_by(Jogos.id).all()
    return render_template('index.html', title='Jogos', game_list=game_list)


@bp.route('/novo-jogo', methods=['GET', 'POST'])
def new_game():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect('/login?next-page=/novo-jogo')
    if request.method == 'POST':
        form = FormGame(request.form)
        if not form.validate_on_submit():
            return render_template(
                'form.html', title='Cadastrar Jogo', form=form
            )
        name = form.name.data
        category = form.category.data
        console = form.console.data
        game_db = Jogos.query.filter_by(nome=name).first()
        if game_db:
            flash('Jogo já cadastrado!')
            return redirect(url_for('views.new_game'))
        new_game = Jogos(nome=name, categoria=category, console=console)
        db.session.add(new_game)
        db.session.commit()
        file = request.files['imagem']
        if file:
            file.save(f'src/static/images/{new_game.id}.jpg')
        flash('Jogo cadastrado com sucesso!')
        return redirect(url_for('views.home'))
    return render_template(
        'form.html', title='Cadastrar Jogo', form=FormGame()
    )


@bp.route('/atualizar/<int:game_id>', methods=['GET', 'POST'])
def update_game(game_id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(f'/login?next-page=/atualizar/{game_id}')
    if request.method == 'POST':
        form = FormGame(request.form)
        if not form.validate_on_submit():
            game = Jogos.query.get(game_id)
            game_cover = return_image(game.id)
            return render_template(
                'form.html',
                title='Atualizar Jogo',
                game=game,
                game_cover=game_cover,
                form=form,
            )
        game = Jogos.query.get(game_id)
        game.nome = form.name.data
        game.categoria = form.category.data
        game.console = form.console.data
        db.session.commit()
        db.session.refresh(game)
        file = request.files['imagem']
        if file:
            remove_image(game.id)
            file.save(f'src/static/images/{game.id}.jpg')
        flash('Jogo atualizado com sucesso!')
        return redirect(url_for('views.home'))
    game = Jogos.query.get(game_id)
    game_cover = return_image(game.id)
    return render_template(
        'form.html',
        title='Atualizar Jogo',
        game=game,
        game_cover=game_cover,
        form=FormGame(),
    )


@bp.route('/deletar/<int:game_id>')
def delete_game(game_id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(f'/login?next-page=/deletar/{game_id}')
    game = Jogos.query.get(game_id)
    db.session.delete(game)
    db.session.commit()
    flash('Jogo deletado com sucesso!')
    return redirect(url_for('views.home'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = FormUser(request.form)
        user_db = Usuarios.query.filter_by(username=form.username.data).first()
        if user_db and bcrypt.check_password_hash(
            user_db.senha, form.password.data
        ):
            session['usuario_logado'] = user_db.username
            flash(user_db.username + ' logado com sucesso!')
            next_page = request.form.get(
                'next-page',
            )
            return redirect(next_page)
        flash('Usuário ou senha inválidos!')
        return redirect(url_for('views.home'))
    next_page = request.args.get(
        'next-page',
    )
    return render_template(
        'login.html', title='Login', next_page=next_page, form=FormUser()
    )


@bp.route('/logout')
def logout():
    session.pop('usuario_logado', None)
    flash('Usuário deslogado com sucesso!')
    return redirect(url_for('views.login'))


@bp.route('/image/<filename>')
def image(filename):
    print(f'Serving image: {filename}')
    print(f'__file__: {__file__}')
    images_dir = os.path.join(
        os.path.dirname(__file__), '..', 'static', 'images'
    )
    print(f'Images directory: {images_dir}')
    return send_from_directory(images_dir, filename)
