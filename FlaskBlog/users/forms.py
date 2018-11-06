import flask
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from FlaskBlog.models import User


class RegistrationForm(FlaskForm):
    ## Setting field label and validators
    username = StringField('Username', validators =
                           [DataRequired(), Length(min = 2, max = 16)])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators =
                             [DataRequired(), Length(min = 8, max = 32)])
    confirm_password = PasswordField('Confirm Password', validators =
                                     [DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError(f"Username {username.data} has already been taken. Please try again.")

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError(f"Email {email.data} has already been taken. Please try again.")


class LoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators =
                             [DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class AccountUpdateForm(FlaskForm):
    username = StringField('Username', validators =
                           [DataRequired(), Length(min = 2, max = 16)])
    email = StringField('Email', validators = [DataRequired(), Email()])
    picture_file = FileField('Update Profile Picture', validators = [FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError(f"Username {username.data} has already been taken. Please try again.")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if email:
                raise ValidationError(f"Email {email.data} has already been taken. Please try again.")


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    submit = SubmitField('Reset Password')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is None:
            raise ValidationError(f"There is no account linked with the email {email.data}.")


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators =
                             [DataRequired(), Length(min = 8, max = 32)])
    confirm_password = PasswordField('Confirm Password', validators =
                                     [DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')