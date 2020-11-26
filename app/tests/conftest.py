import os
import os.path as op

import pytest

from app import create_app, db
from app.models import PowerUnit


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
    def _add_power_unit(power_unit, notes):
        power_unit = PowerUnit(power_unit=power_unit, notes=notes)
        db.session.add(power_unit)
        db.session.commit()
        return power_unit
    return _add_power_unit
