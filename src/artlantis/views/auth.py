import secrets
from PIL import Image
from flask import (
    Blueprint, redirect, request, render_template, flash, url_for)
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import (current_user, login_user, logout_user)
from flask_mail import Message

from artlantis import db, mail, bcrypt
from artlantis.forms import (
    RegistrationForm, RequestResetForm, LoginForm, ResetPasswordForm)
from artlantis.models import User
from artlantis.views.helper_fns import send_mail

auth = Blueprint(
    'auth', __name__, template_folder='templates')

@auth.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
                            form.password.data).decode('utf-8')
        user = User(username=form.username.data, 
                    email=form.email.data, 
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in',
                                                                 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register', form=form)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
                                user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(
                                                    url_for('main.home'))
        flash('Login Unsuccessful. Please check email and password', 
                                                            'danger')
    return render_template('login.html', title='Login', form=form)

@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

def send_reset_email(user):
    token = user.get_reset_token()
    header = "Password Reset Request"
    body = f'''To reset your password, visit the following link:
{url_for('auth.reset_token', token=token, _external=True)}

If you did not make this request, simply ignore this email and no changes will be made.
'''
    send_mail([user.email], "noreply@demo.com", header, body)

@auth.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password',
                                                                         'info')
        return redirect(url_for('auth.login'))
    return render_template(
        'reset_request.html', title='Reset Password', form=form)

@auth.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('auth.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
                        form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated! You are now able to log in', 
                                                                    'success')
        return redirect(url_for('auth.login'))
    return render_template(
        'reset_token.html', title='Reset Password', form=form)

