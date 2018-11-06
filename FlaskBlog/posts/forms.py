import flask
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from FlaskBlog.models import User


class PostForm(FlaskForm):
    title = StringField('Title', validators = [DataRequired()])
    address = TextAreaField('Address', validators = [DataRequired()])
    submit = SubmitField('Post')