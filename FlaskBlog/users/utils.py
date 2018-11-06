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



def save_image_file(image_file):
    random_hex = secrets.token_hex(8)
    file_name, file_extension = os.path.splitext(image_file.filename)
    final_name = random_hex + file_extension
    image_path = os.path.join(current_app.root_path, 'static/profile_pics', final_name)
    output_size = (125, 125)
    resized_image = Image.open(image_file)
    resized_image.thumbnail(output_size)
    resized_image.save(image_path)
    return final_name

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender = 'rachitbhargava99@gmail.com', recipients = [user.email])
    msg.body = f'''To reset your password, kindly visit: {url_for('users.reset', token = token, _external = True)}

Kindly ignore this email if you did not make this request'''
    mail.send(msg)