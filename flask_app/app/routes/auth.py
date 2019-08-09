from app import app, db, login
from flask import (
    redirect, url_for, flash, render_template,
    request
)
from flask_login import current_user, login_user, logout_user

from app.forms.auth import LoginForm
from app.models.auth import User

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(
            (User.username == form.user.data) |
            (User.email == form.user.data)
        ).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username/email or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember.data)
        
        next_page = request.args.get('next')
        if not next_page:
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('auth/login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))