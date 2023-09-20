from flask import render_template
from application import db
from application.errors import bp
from application.main.exceptions import HTTPError404


@bp.app_errorhandler(404)
@bp.app_errorhandler(HTTPError404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@bp.app_errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500
