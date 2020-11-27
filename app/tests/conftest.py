import os
import os.path as op

import pytest

from app import create_app, db
from app.models import User, PowerUnit, PowerUnitMeta


@pytest.fixture(scope='module')
def test_app():
    app = create_app()
    app.config.from_object('app.config.TestingConfig')
    with app.app_context():
        yield app  # testing happens here


@pytest.fixture(scope='module')
def test_database():    
    # Remove any existing database
    # app_dir = op.realpath(os.path.dirname(__file__))
    # database_path = op.join(app_dir, app.config['DATABASE_FILE'])
    # if os.path.exists(database_path):
    #     os.remove(database_path)

    db.drop_all()
    db.create_all()
    yield db  # testing happens here
    db.session.remove()
    db.drop_all()


@pytest.fixture(scope='function')
def add_power_unit():
    def _inner_func(power_unit, notes):
        record = PowerUnit(power_unit=power_unit, notes=notes)
        db.session.add(record)
        db.session.commit()
        return record
    return _inner_func


@pytest.fixture(scope='function')
def add_power_units_meta():
    def _inner_func(**kwargs):
        record = PowerUnitMeta()
        for key, value in kwargs.items():
            setattr(record, key, value)
        db.session.add(record)
        db.session.commit()
        return record
    return _inner_func


@pytest.fixture(scope='module')
def add_user():
    def _add_user(name, email, password):
        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return user
    return _add_user