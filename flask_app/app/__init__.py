from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_security import SQLAlchemyUserDatastore, Security

from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.models import auth_models, radius_models
# setup flask-security
user_datastore = SQLAlchemyUserDatastore(db, auth_models.User, auth_models.Role)
security = Security(app, user_datastore)

from app import routes