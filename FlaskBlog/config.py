import os

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY')
	SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
	MAIL_SERVER = os.environ.get('MAIL_SERVER')
	MAIL_PORT = int(os.environ.get('MAIL_PORT'))
	MAIL_USE_TLS = bool(os.environ.get('MAIL_USE_TLS'))
	MAIL_USERNAME = os.environ.get('EMAIL_USER')
	MAIL_PASSWORD = os.environ.get('EMAIL_PASS')