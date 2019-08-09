from app import app, db
from flask import render_template
from flask_login import login_required

from app.models.auth import User

@app.before_first_request
def setup():
    # create admin user
    if not User.query.count():
        admin = User(username='admin', password='admin')
        admin.hash_password()
        db.session.add(admin)
        db.session.commit()

@app.route('/')
@login_required
def index():
    return render_template(
        'base.html'
    )