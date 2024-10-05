from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel


app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)


def get_locale():
    override = request.args.get('lang')

    if override:
        session['lang'] = override

    return session.get('lang', 'en')

# Initialize babel
babel = Babel(app, locale_selector=get_locale)


# Initialize babel
babel = Babel(app, locale_selector=get_locale)


import admin.main
