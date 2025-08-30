from flask import Flask, render_template

app = Flask(__name__)


class Game:
    def __init__(self, name, category, console):
        self.name = name
        self.category = category
        self.console = console


@app.route('/')
def home():
    game1 = Game('God of War', 'Ação', 'PlayStation')
    game2 = Game('Skyrim', 'RPG', 'PC')
    game3 = Game('Valorant', 'Tiro', 'PC')
    game_list = [game1, game2, game3]
    return render_template('list.html', title='Jogos', game_list=game_list)
