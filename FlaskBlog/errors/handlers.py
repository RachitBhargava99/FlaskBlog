from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
	return render_template('errors/404.html', title = "404 Not Found"), 404

@errors.app_errorhandler(403)
def error_404(error):
	return render_template('errors/403.html', title = "403 Not Authorized"), 403

@errors.app_errorhandler(500)
def error_404(error):
	return render_template('errors/500.html', title = "500 Server Error"), 500