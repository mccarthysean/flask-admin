
import os
import time
import jwt
import datetime

from flask import current_app
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import mapper
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db, login_manager, bcrypt


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class PowerUnit(db.Model):
    """Create a public.power_units table representation"""

    __tablename__ = 'power_units'
    # __table_args__ = {"schema": "public"}

    id = db.Column(Integer, primary_key=True)
    power_unit = db.Column(Integer, nullable=False, unique=True)
    notes = db.Column(String)

    def __repr__(self):
        return f'{self.power_unit}'


def create_meta_class(base_model, meta_model, db_table_name):
    """Given a regular base model, and a meta model to be filled out, 
    return the filled out meta model for the base model's metadata"""
    global db

    cols = [Column(name, String) for name in base_model.__mapper__.attrs.keys() if name != 'id']
    cols.insert(0, db.Column("id", Integer, primary_key=True))
    cols.insert(1, db.Column("id_foreign", Integer, db.ForeignKey(base_model.id, ondelete="CASCADE"), nullable=False))
    cols.insert(2, db.Column("element", String, nullable=False))
    tbl = Table(db_table_name, db.metadata, *cols)
    mapper(meta_model, tbl)

    return None


class PowerUnitMeta:
    query = db.session.query_property()
    pass


create_meta_class(PowerUnit, PowerUnitMeta, 'power_units_meta')


class MetaData(db.Model):
    __tablename__ = 'meta_data'

    # id = db.Column("id", Integer, primary_key=True)
    id_cell = db.Column(String, primary_key=True)
    element = db.Column(String, nullable=False)
    color = db.Column(String, nullable=False)

    def __repr__(self):
        return f'{self.id_cell}'


class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False

    @staticmethod
    def save_token(token):
        blacklist_token = BlacklistToken(token=token)
        try:
            # insert the token
            db.session.add(blacklist_token)
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': 'Successfully logged out.'
            }
            return response_object, 200
        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': e
            }
            return response_object, 200


class User(UserMixin, db.Model):
    """
    Create a User table
    """

    __tablename__ = 'users'

    id = db.Column(Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(String(60), unique=True, nullable=False)
    # active = db.Column(db.Boolean(), default=True, nullable=False)
    created_date = db.Column(db.DateTime, default=func.now())
    password = db.Column(String(128), nullable=False)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(
            password,
            current_app.config.get('BCRYPT_LOG_ROUNDS')
        )

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.set_password(password)

    # @property
    # def password(self):
    #     """
    #     Prevent password from being accessed
    #     """
    #     raise AttributeError('password is not a readable attribute.')
    #     # return self.password_hash
    #     # return self.password

    # @password.setter
    # def password(self, password):
    #     """
    #     Set password to a hashed password
    #     """
    #     self.password_hash = generate_password_hash(
    #         password,
    #         current_app.config.get('BCRYPT_LOG_ROUNDS')
    #     )

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time.time() + expires_in},
            os.getenv('SECRET_KEY'), 
            algorithm='HS256'
        ).decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(
                token, 
                os.getenv('SECRET_KEY'),
                algorithms=['HS256']
            )['reset_password']
        except:
            return
        return User.query.get(id)

    def __repr__(self):
        # return '<User: {}>'.format(self.name)
        return str(self.email)

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                current_app.config['SECRET_KEY'],
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(
                auth_token, 
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

