from flask import Flask, redirect, render_template, request

app = Flask(__name__)


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
def create():
    return render_template('form.html', title='Cadastrar Jogo')


@app.route('/cadastrar-jogo', methods=['POST'])
def create_game():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    novo_jogo = Game(nome, categoria, console)
    game_list.append(novo_jogo)
    return redirect('/')


app.run(debug=True)
