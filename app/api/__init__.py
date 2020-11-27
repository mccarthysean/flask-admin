# from flask import Blueprint

# bp = Blueprint('api', __name__)

# from app.api import users, errors, tokens

from flask_restx import Api

from app.api.ping import ping_namespace
from app.api.auth import auth_namespace
from app.api.users import users_namespace
from app.api.power_units import power_units_namespace
from app.api.power_units_meta import power_units_meta_namespace
from app.api.meta_data import meta_data_namespace


api = Api(
    version='1.0', 
    title='IJACK MetaData API', 
    description="For Flask-Admin views' metadata", 
    # doc="/docs/"
)

api.add_namespace(ping_namespace, path="/ping")
api.add_namespace(auth_namespace, path="/auth")
api.add_namespace(users_namespace, path="/users")
api.add_namespace(power_units_namespace, path="/power_units")
api.add_namespace(power_units_meta_namespace, path="/power_units_meta")
api.add_namespace(meta_data_namespace, path="/meta_data")
