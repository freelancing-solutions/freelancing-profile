
from flask import render_template, Blueprint
from .. import cache
from ..library import Metatags
from werkzeug.exceptions import BadRequest, Forbidden, NotFound, MethodNotAllowed, Unauthorized, HTTPException
from ..library.utils import const

error_blueprint = Blueprint('error', __name__)

###########################################################################################################
# Error Handlers


# cached for 24 hours
@error_blueprint.app_errorhandler(BadRequest)
@cache.cached(timeout=const.cache_timeout_hour*24)
def handle_bad_request(e: BadRequest) -> tuple:
    title: str = "Bad Request"
    return render_template('error.html', heading=title, message={e.name},
                           meta_tags=Metatags().set_home()), e.code


@error_blueprint.app_errorhandler(Forbidden)
@cache.cached(timeout=const.cache_timeout_hour*24)
def handle_forbidden(e: Forbidden) -> tuple:
    title: str = "Request Forbidden"
    return render_template('error.html', heading=title,  message={e.name},
                           meta_tags=Metatags().set_home()), e.code


@error_blueprint.app_errorhandler(NotFound)
@cache.cached(timeout=const.cache_timeout_hour*24)
def handle_not_found(e: NotFound) -> tuple:
    title: str = "Page not Found"
    return render_template('404.html', heading=title,  message={e.name},
                           meta_tags=Metatags().set_home()), e.code


@error_blueprint.app_errorhandler(MethodNotAllowed)
@cache.cached(timeout=const.cache_timeout_hour*24)
def handle_not_allowed(e: MethodNotAllowed) -> tuple:
    title: str = "Method Not Allowed"
    return render_template('error.html', heading=title,  message={e.name},
                           meta_tags=Metatags().set_home()), e.code


@error_blueprint.app_errorhandler(Unauthorized)
@cache.cached(timeout=const.cache_timeout_hour*24)
def handle_unauthorized(e: Unauthorized) -> tuple:
    title: str = "Not Authorized"
    return render_template('error.html', heading=title, message={e.name},
                           meta_tags=Metatags().set_home()), e.code


@error_blueprint.app_errorhandler(HTTPException)
@cache.cached(timeout=const.cache_timeout_hour*24)
def handle_exception(e: HTTPException) -> tuple:
    title: str = "Request Error"
    return render_template('error.html', heading=title, message={e.name},
                           meta_tags=Metatags().set_home()), e.code


@error_blueprint.route('/debug-sentry')
@cache.cached(timeout=const.cache_timeout_hour*24)
def trigger_sentry():
    division_by_zero = 1 / 0

