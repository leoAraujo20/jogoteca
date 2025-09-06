import os

from dotenv import load_dotenv
from flask import Flask

from extension import db

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db.init_app(app)

# evitar importação circular
from views.views import *  # noqa: E402, F403

if __name__ == '__main__':
    app.run(debug=True)
