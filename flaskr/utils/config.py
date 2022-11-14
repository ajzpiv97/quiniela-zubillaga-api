from flaskr.utils.env_variables import SECRET_KEY as SECRET_KEY_ENCRYPTION
from flaskr.utils.utils import modify_database_url_to_add_dialect


class Config:
    """Base config."""
    SECRET_KEY = SECRET_KEY_ENCRYPTION
    SQLALCHEMY_DATABASE_URI = modify_database_url_to_add_dialect()


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
