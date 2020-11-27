from flask import request
from flask_restx import Resource, fields, Namespace

from app import db
from app.models import User
from app.api.crud import (  # isort:skip
    get_all_users,
    get_user_by_email,
    add_user,
    get_user_by_id,
    update_user,
    delete_user,
)


users_namespace = Namespace('users')

user_model = users_namespace.model(
    'User', {
        'id': fields.Integer(readOnly=True),
        'name': fields.String(required=True),
        'email': fields.String(required=True),
        'created_date': fields.DateTime,
    }
)

user_post_model = users_namespace.inherit("User post", user_model, {
    "password": fields.String(required=True)
})


class UsersList(Resource):

    @users_namespace.marshal_with(user_model, as_list=True)
    def get(self):
        return get_all_users(), 200

    @users_namespace.expect(user_post_model, validate=True)
    def post(self):
        post_data = request.get_json()
        name = post_data.get('name')
        email = post_data.get('email')
        password = post_data.get("password")
        response_object = {}

        record = get_user_by_email(email)
        if record:
            response_object['message'] = 'Sorry. That email already exists.'
            return response_object, 400

        add_user(name, email, password)

        response_object['message'] = f'{email} was added!'
        return response_object, 201


class Users(Resource):

    @users_namespace.marshal_with(user_model)
    @users_namespace.response(200, "Success")
    @users_namespace.response(404, "User <user_id> does not exist")
    def get(self, user_id):
        """Returns a single user."""
        record = get_user_by_id(user_id)
        if not record:
            users_namespace.abort(404, f"User {user_id} does not exist")
        return record, 200

    @users_namespace.expect(user_model, validate=True)
    @users_namespace.response(200, "<user_id> was updated!")
    @users_namespace.response(400, "Sorry. That email already exists.")
    @users_namespace.response(404, "User <user_id> does not exist")
    def put(self, user_id):
        """Updates a user."""
        post_data = request.get_json()
        name = post_data.get("name")
        email = post_data.get("email")
        response_object = {}

        record = get_user_by_id(user_id)
        if not record:
            users_namespace.abort(404, f"User {user_id} does not exist")

        if get_user_by_email(email):
            response_object["message"] = "Sorry. That email already exists."
            return response_object, 400

        update_user(record, name, email)

        response_object["message"] = f"{record.id} was updated!"
        return response_object, 200

    @users_namespace.response(200, "<user_id> was removed!")
    @users_namespace.response(404, "User <user_id> does not exist")
    def delete(self, user_id):
        """Deletes a user"""
        response_object = {}
        record = get_user_by_id(user_id)

        if not record:
            users_namespace.abort(404, f"User {user_id} does not exist")

        delete_user(record)

        response_object["message"] = f"{record.email} was removed!"
        return response_object, 200


users_namespace.add_resource(UsersList, '')
users_namespace.add_resource(Users, '/<int:user_id>')
