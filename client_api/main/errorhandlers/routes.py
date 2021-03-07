
from flask import render_template, request, make_response, Blueprint
from ..library import Metatags
from werkzeug.exceptions import BadRequest, Forbidden,NotFound,MethodNotAllowed,Unauthorized

error_blueprint = Blueprint('error', __name__)

###########################################################################################################
# Error Handlers

@error_blueprint.app_errorhandler(BadRequest)
def handle_bad_request(e):
    return render_template('error.html', heading="Bad Request", meta_tags=Metatags().set_home())

@error_blueprint.app_errorhandler(Forbidden)
def handle_forbidden(e):
    return render_template('error.html', heading="Request Forbidden", meta_tags=Metatags().set_home())

@error_blueprint.app_errorhandler(NotFound)
def handle_not_found(e):
    return render_template('404.html', heading="Page Not Found", meta_tags=Metatags().set_home())

@error_blueprint.app_errorhandler(MethodNotAllowed)
def handle_not_allowed(e):
    return render_template('error.html', heading="Request Method not allowed for this resource", meta_tags=Metatags().set_home())

@error_blueprint.app_errorhandler(Unauthorized)
def handle_unauthorized(e):
    return render_template('error.html', heading="You are not authorized to make this request", meta_tags=Metatags().set_home())

@error_blueprint.route('/debug-sentry')
def trigger_sentry():
    division_by_zero = 1 / 0