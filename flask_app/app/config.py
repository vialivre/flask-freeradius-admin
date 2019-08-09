import os

basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE_SERVER = os.getenv('DATABASE_SERVER')
DATABASE_PORT = os.getenv('DATABASE_PORT', '5432')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_NAME = os.getenv('DATABASE_NAME')
DB_URI = 'postgresql+psycopg2://{user}:{psswd}@{server}:{port}/{db}'.format(
    user=DATABASE_USER,
    psswd=DATABASE_PASSWORD,
    server=DATABASE_SERVER,
    port=DATABASE_PORT,
    db=DATABASE_NAME
)

class Config(object):
    SECRET_KEY = 'flask-freeradius-admin-secret'

    SECURITY_RECOVERABLE = True
    SECURITY_CHANGEABLE = True
    SECURITY_USER_IDENTITY_ATTRIBUTES = ['username', 'email']

    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False