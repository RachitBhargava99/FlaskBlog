import secrets
import os
from PIL import Image
from flask import Flask, render_template, url_for, flash, redirect, request, abort, current_app
from FlaskBlog.users.forms import RegistrationForm, LoginForm, AccountUpdateForm, RequestResetForm, ResetPasswordForm
from FlaskBlog.posts.forms import PostForm
from FlaskBlog.models import User, Post
from flask_wtf.file import FileField, FileAllowed
from FlaskBlog import db, bcrypt, mail
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


from flask import Blueprint

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', default = 1, type = int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page = 5)
    return render_template('home.html', posts = posts)

@main.route('/about')
def about():
    return render_template('about.html')