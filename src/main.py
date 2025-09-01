from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

app = Flask(__name__)
app.secret_key = 'jogoteca'


class Game:
    def __init__(self, name, category, console):
        self.name = name
        self.category = category
        self.console = console


game1 = Game('God of War', 'Ação', 'PlayStation')
game2 = Game('Skyrim', 'RPG', 'PC')
game3 = Game('Valorant', 'Tiro', 'PC')
game_list = [game1, game2, game3]


@app.route('/')
def home():
    return render_template('index.html', title='Jogos', game_list=game_list)


@app.route('/novo-jogo', methods=['GET'])
def new_game():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect('/login?next-page=/novo-jogo')
    return render_template('form.html', title='Cadastrar Jogo')


@app.route('/cadastrar-jogo', methods=['POST'])
def create_game():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    novo_jogo = Game(nome, categoria, console)
    game_list.append(novo_jogo)
    return redirect(url_for('home'))


@app.route('/login')
def login():
    return render_template('login.html', title='Login')


@app.route('/autenticar', methods=['POST'])
def authenticate():
    if 'secret' == request.form['senha']:
        session['usuario_logado'] = request.form['usuario']
        next_page = request.form.get('next-page')
        flash(f'Usuário {session["usuario_logado"]} logado com sucesso!')
        return redirect(next_page)
    else:
        flash('Usuário ou senha inválidos.')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('usuario_logado', None)
    flash('Usuário deslogado com sucesso!')
    return redirect(url_for('login'))


app.run(debug=True)
