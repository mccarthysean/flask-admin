
import os
import os.path as op
import pathlib
import logging

# third-party imports
from flask import current_app, Flask, render_template, render_template_string, send_from_directory, request, url_for, jsonify
import flask_admin
from flask_admin import Admin
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager, current_user
from werkzeug.middleware.proxy_fix import ProxyFix

db = SQLAlchemy()
cors = CORS()
bcrypt = Bcrypt()
login_manager = LoginManager()


def seed_db(app):
    """Populate a small db with some example entries"""

    from app.models import PowerUnit, PowerUnitMeta, MetaData, User

    # Add some sample power units
    power_units = [200123, 200321, 200456, 200789]
    notes = ["test1", "test2", "test3", "test4"]

    # Add some metadata about those power units' rows/columns
    power_unit_ids = [1, 2, 3, 4]
    elements = ["text color", "fill color", "text color", "fill color"]
    notes = ["this is a fake note" for i in range(4)]

    pu_colors = ["#F9F9F9", "#717174", "#F9F9F9", "#717174"]
    notes_colors = ["#292929", "#668AAA", "#292929", "#668AAA"]

    with app.app_context():
        db.drop_all()
        db.create_all()

        for i in range(4):
            # Add some sample power units
            pu = PowerUnit()
            pu.power_unit = power_units[i]
            pu.notes = notes[i]
            db.session.add(pu)

            # Add some metadata about those power units' rows/columns
            pum = PowerUnitMeta()
            pum.id_foreign = power_unit_ids[3 - i]
            pum.element = elements[i]
            pum.power_unit = pu_colors[i]
            pum.notes = notes_colors[i]
            db.session.add(pum)

            # md = MetaData()
            # md.id_cell = power_unit_ids[3 - i]
            # md.element = elements[i]
            # md.color = pu_colors[3 - i]
            # db.session.add(md)

        user = User(
            name="Sean McCarthy",
            email="sean.mccarthy@hotmail.com",
            password="test"
        )
        db.session.add(user)

        db.session.commit()

    return


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


def create_app():
    """Factory pattern"""

    # Create flask app
    app = Flask(
        __name__, 
        # template_folder='templates',
        instance_path=str(pathlib.Path(__file__).parent.joinpath("instance")),
    )
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)
    app.config.from_object('app.config.DevelopmentConfig')
    logging.basicConfig(level=logging.DEBUG)
    # app.debug = True

    # Initialize extensions
    db.init_app(app) # SQLAlchemy
    cors.init_app(app, resources={r"*": {"origins": "*"}})
    bcrypt.init_app(app)

    # Register api
    from app.api import api
    api.init_app(app)

    # Build a sample db on the fly
    app_dir = op.realpath(os.path.dirname(__file__))
    database_path = op.join(app_dir, app.config['DATABASE_FILE'])
    # if os.path.exists(database_path):
    #     os.remove(database_path)
    #     seed_db(app)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    # Flask views
    @app.route('/')
    def index():
        # return """<a href="/admin/">Click here to get to the admin views</a>"""
        return render_template_string("""
            <html><body>
                <a href="/admin/">Click here to get to the admin views</a><br>
                <a href="/docs/">Click here to go to the API documentation</a>
            </html></body>
        """)

    @app.route('/test/', methods=['GET', 'POST'])
    def test():
        return render_template('test.html')

    @app.route('/hello/', methods=['GET', 'POST'])
    def hello():
        # POST request
        if request.method == 'POST':
            current_app.logger.debug('Incoming..')
            current_app.logger.debug(request.get_json())  # parse as JSON
            return 'OK', 200

        # GET request
        else:
            message = {'greeting': 'Hello from Flask!'}
            return message  # serialize and use JSON headers

    # Add the database 'models' (tables) to the admin page
    from app.models import PowerUnit, PowerUnitMeta, User, MetaData
    from app.admin import SecuredAdminIndexView, PowerUnitView, PowerUnitMetaView, UserView, MetaDataView

    # Create admin interface
    flask_adm = Admin(app, name='IJACK', template_mode='bootstrap3', 
        index_view=SecuredAdminIndexView(name='Admin', url='/admin', endpoint='admin')
    )
    flask_adm.add_view(UserView(User, db.session, name='Users', endpoint='admin.users'))
    flask_adm.add_view(PowerUnitView(PowerUnit, db.session, name='Power Units', endpoint='admin.power_units'))
    flask_adm.add_view(PowerUnitMetaView(PowerUnitMeta, db.session, name='Power Unit Meta', endpoint='admin.power_units_meta'))
    flask_adm.add_view(MetaDataView(MetaData, db.session, name='Meta Data', endpoint='admin.meta_data'))

    return app

