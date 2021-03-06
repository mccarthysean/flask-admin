import unittest
import datetime

from app import db
from app.models import User


def test_encode_token(test_app, test_database, add_user):
    test_database.session.query(User).delete()
    user = add_user('justatest', 'test@test.com', 'test')
    token = user.encode_token(user.id, 'access')
    assert isinstance(token, bytes)


def test_decode_token(test_app, test_database, add_user):
    test_database.session.query(User).delete()
    user = add_user('justatest', 'test@test.com', 'test')
    token = user.encode_token(user.id, 'access')
    assert isinstance(token, bytes)
    assert User.decode_token(token) == user.id


def test_passwords_are_random(test_app, test_database, add_user):
    """This won't work if passwords are not readable"""
    test_database.session.query(User).delete()
    user_one = add_user('justatest', 'test@test.com', 'greaterthaneight')
    user_two = add_user('justatest2', 'test@test2.com', 'greaterthaneight')
    assert user_one.password != user_two.password


def test_encode_auth_token(test_app, test_database):
    test_database.session.query(User).delete()
    user = User(
        email='test@test.com',
        name="Sean",
        password='test',
    )
    test_database.session.add(user)
    test_database.session.commit()
    auth_token = user.encode_auth_token(user.id)
    assert isinstance(auth_token, bytes)


def test_decode_auth_token(test_app, test_database):
    test_database.session.query(User).delete()
    user = User(
        email='test@test.com',
        name="Sean",
        password='test',
    )
    test_database.session.add(user)
    test_database.session.commit()
    auth_token = user.encode_auth_token(user.id)
    assert isinstance(auth_token, bytes)
    assert User.decode_auth_token(auth_token.decode("utf-8")) == 1


if __name__ == '__main__':
    unittest.main()