from app import app, db
from flask import render_template

@app.before_first_request
def setup():
    # create admin user
    pass

@app.route('/')
def index():
    return render_template(
        'base.html'
    )