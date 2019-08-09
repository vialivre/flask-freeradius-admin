from app import app, db, user_datastore
from flask import render_template
from flask_security import login_required, current_user

@app.before_first_request
def setup():
    if not user_datastore.get_user(1):
        # create admin user
        db.create_all()
        user_datastore.create_user(username='admin', password='admin')
        db.session.commit()

@app.route('/')
@login_required
def index():
    print(current_user)
    return render_template(
        'base.html',
        user=current_user
    )