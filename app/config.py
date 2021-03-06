

class BaseConfig:
    TESTING = False

    # Create in-memory database
    DATABASE_FILE = 'sample_db.sqlite'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_FILE
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'fdshjak54372816&*((hfjdkslahklhkjfhdsjkahfjdhskaf'
    BCRYPT_LOG_ROUNDS = 13
    ACCESS_TOKEN_EXPIRATION = 900       # 15 minutes
    REFRESH_TOKEN_EXPIRATION = 2592000  # 30 days


class DevelopmentConfig(BaseConfig):
    FLASK_ENV = 'development'
    BCRYPT_LOG_ROUNDS = 4


class TestingConfig(BaseConfig):
    FLASK_ENV = 'testing'
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    ACCESS_TOKEN_EXPIRATION = 3
    REFRESH_TOKEN_EXPIRATION = 3


class ProductionConfig(BaseConfig):
    pass


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)
