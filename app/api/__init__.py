# from flask import Blueprint

# bp = Blueprint('api', __name__)

# from app.api import users, errors, tokens

from flask_restx import Api

from app import db
from app.api.ping import ping_namespace
from app.api.power_units import power_units_namespace
from app.api.power_units_meta import power_units_meta_namespace

api = Api(version='1.0', title='IJACK MetaData API', description="For Flask-Admin views' metadata")

api.add_namespace(ping_namespace, path="/ping")
api.add_namespace(power_units_namespace, path="/power_units")
api.add_namespace(power_units_meta_namespace, path="/power_units_meta")

