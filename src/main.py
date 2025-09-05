import os

from dotenv import load_dotenv
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)
app.secret_key = 'jogoteca'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = SQLAlchemy(app)


class Jogos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(40), nullable=False)
    console = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Game {self.nome}>'


class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


@app.route('/')
def home():
    game_list = Jogos.query.all()
    return render_template('index.html', title='Jogos', game_list=game_list)


@app.route('/novo-jogo', methods=['GET'])
def new_game():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect('/login?next-page=/novo-jogo')
    return render_template('form.html', title='Cadastrar Jogo')


@app.route('/cadastrar-jogo', methods=['POST'])
def create_game():
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


@app.route('/login')
def login():
    next_page = request.args.get('next-page')
    print(type(next_page))
    print(next_page)
    return render_template('login.html', title='Login', next_page=next_page)


@app.route('/autenticar', methods=['POST'])
def authenticate():
    user_db = Usuarios.query.filter_by(username=request.form['user']).first()
    if user_db and user_db.senha == request.form['password']:
        session['usuario_logado'] = user_db.username
        flash(user_db.username + ' logado com sucesso!')
        next_page = request.form['next-page']
        return redirect(next_page)
    flash('Usuário ou senha inválidos!')
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('usuario_logado', None)
    flash('Usuário deslogado com sucesso!')
    return redirect(url_for('login'))


app.run(debug=True)
