import os

from dotenv import load_dotenv
from flask import Flask
from flask_wtf.csrf import CSRFProtect

from .extension import bcrypt, db  # Importa as extensões do nosso ficheiro


def create_app():
    """
    Cria e configura a instância da aplicação Flask (Application Factory).
    """
    # Carrega as variáveis de ambiente
    load_dotenv()

    # Cria a instância da app
    app = Flask(__name__, instance_relative_config=True)

    # Carrega as configurações
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

    # Inicializa as extensões com a app
    db.init_app(app)
    bcrypt.init_app(app)
    CSRFProtect(app)

    from src.views.views import bp

    app.register_blueprint(bp)

    return app
