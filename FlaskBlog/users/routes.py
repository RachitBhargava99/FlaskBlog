import secrets
import os
from PIL import Image
from flask import Flask, render_template, url_for, flash, redirect, request, abort, current_app
from FlaskBlog.users.forms import RegistrationForm, LoginForm, AccountUpdateForm, RequestResetForm, ResetPasswordForm
from FlaskBlog.posts.forms import PostForm
from FlaskBlog.users.utils import save_image_file, send_reset_email
from FlaskBlog.models import User, Post
from flask_wtf.file import FileField, FileAllowed
from FlaskBlog import db, bcrypt, mail
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


from flask import Blueprint

users = Blueprint('users', __name__)

@users.route('/register', methods = ['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}.', 'success')
        return redirect(url_for('main.home'))
    return render_template('register.html', title = 'Register', form = form)

@users.route('/login', methods = ['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Log In Unsuccessful. Please check the provided email and password', 'danger')
    return render_template('login.html', title = 'Login', form = form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route('/account', methods = ['POST', 'GET'])
@login_required
def account():
    form = AccountUpdateForm()
    if form.validate_on_submit():
        if form.picture_file.data:
            image_file_name = save_image_file(form.picture_file.data)
            current_user.image_file = image_file_name
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f"Information for username { current_user.username } has been updated successfully!", 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file_address = url_for('static', filename = 'profile_pics/' + current_user.image_file)
    return render_template('account.html', title = 'Account', image_file = image_file_address, user = current_user, form = form)

@users.route('/reset_password', methods = ['GET', 'POST'])
def request_reset():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash(f"Please check your inbox for an email with instructions to reset the password.")
        return redirect(url_for('users.login'))
    return render_template('request_reset.html', title = "Request Reset Password", form = form)

@users.route('/reset/<token>', methods = ['GET', 'POST'])
def reset(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash(f"Sorry, the link is invalid or has expired!", 'warning')
        return redirect(url_for('users.request_reset'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pwd
        db.session.commit()
        flash(f'Password has been reset for the username {user.username}.', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset.html', title = "Reset Password", form = form)

@users.route('/author/<string:author_un>')
def author_page(author_un):
    page = request.args.get('page', 1, type = int)
    user = User.query.filter_by(username = author_un).first_or_404()
    posts = Post.query.filter_by(author = user)\
        .order_by(Post.date_posted.desc())\
        .paginate(per_page = 5)
    return render_template('user_posts.html', posts = posts, user = user)