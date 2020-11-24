
import os
import os.path as op
import pathlib
import logging

# third-party imports
from flask import Flask, render_template, send_from_directory, request, url_for
import flask_admin
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class MyAdminView(flask_admin.BaseView):
    """Create custom admin view"""

    @flask_admin.expose('/')
    def index(self):
        return self.render('myadmin.html')


class AnotherAdminView(flask_admin.BaseView):
    @flask_admin.expose('/')
    def index(self):
        return self.render('anotheradmin.html')

    @flask_admin.expose('/test/')
    def test(self):
        return self.render('test.html')


def build_sample_db(app):
    """Populate a small db with some example entries"""

    from app.models import PowerUnit

    power_units = [200123, 200321, 200456, 200789]
    notes = ["test1", "test2", "test3", "test4"]

    with app.app_context():
        db.drop_all()
        db.create_all()

        for i in range(4):
            pu = PowerUnit()
            pu.power_unit = power_units[i]
            pu.notes = notes[i]
            db.session.add(pu)

        db.session.commit()

    return


def create_app():
    """Factory pattern"""

    # Create flask app
    app = Flask(
        __name__, 
        template_folder='templates',
        instance_path=str(pathlib.Path(__file__).parent.joinpath("instance")),
    )
    logging.basicConfig(level=logging.DEBUG)
    app.debug = True

    # Create in-memory database
    app.config['DATABASE_FILE'] = 'sample_db.sqlite'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'fdshjak54372816&*((hfjdkslahklhkjfhdsjkahfjdhskaf'

    # Initialize extensions
    db.init_app(app) # SQLAlchemy

    # Build a sample db on the fly
    app_dir = op.realpath(os.path.dirname(__file__))
    database_path = op.join(app_dir, app.config['DATABASE_FILE'])
    # if os.path.exists(database_path):
    #     os.remove(database_path)
    if not os.path.exists(database_path):
        build_sample_db(app)

    # Flask views
    @app.route('/')
    def index():
        return '<a href="/admin/">Click me to get to Admin!</a>'

    # Add the database 'models' (tables) to the admin page
    from app.models import PowerUnit
    from app.admin import PowerUnitView

    # Create admin interface
    flask_admin = Admin(app, name='IJACK', template_mode='bootstrap3')
    flask_admin.add_view(PowerUnitView(PowerUnit, db.session, category='Units', name='Power Units', endpoint='admin.power_units'))
    # flask_admin.init_app(app)

    return app

