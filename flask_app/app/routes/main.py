from app import app, db
from flask import render_template
from flask_login import login_required

from app.models.auth import User, Group
from app.models.radius import (
    RadGroupCheck, RadGroupReply, RadUserGroup
)

@app.before_first_request
def setup():
    # create admin user
    if not User.query.count():
        admin = User(username='admin', password='admin')
        admin.hash_password()
        db.session.add(admin)
        db.session.commit()

    # create default users groups
    if not Group.query.count():
        db.session.add(Group(name='user', description='Default user group'))
        db.session.add(Group(name='admin', description='Admin user group'))
        db.session.commit()

        # create default parameters for groups
        db.session.add(
            RadUserGroup(username='admin', groupname='admin', priority=1)
        )
        db.session.commit()

@app.route('/')
@login_required
def index():
    return render_template(
        'base.html'
    )