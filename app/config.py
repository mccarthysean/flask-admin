

class BaseConfig:
    TESTING = False

    # Create in-memory database
    DATABASE_FILE = 'sample_db.sqlite'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_FILE
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'fdshjak54372816&*((hfjdkslahklhkjfhdsjkahfjdhskaf'


class DevelopmentConfig(BaseConfig):
    FLASK_ENV = 'development'


class TestingConfig(BaseConfig):
    FLASK_ENV = 'testing'
    TESTING = True


class ProductionConfig(BaseConfig):
    pass
