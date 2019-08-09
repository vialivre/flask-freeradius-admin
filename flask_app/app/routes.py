from app import app, db, login_manager
from flask import render_template
from flask_login import current_user

from app.models.auth_models import User

@app.before_first_request
def setup():
    # create admin user
    if not User.query.count():
        admin = User(username='admin', password='admin')
        db.session.add(admin)
        db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def index():
    return render_template(
        'base.html',
        user=current_user
    )