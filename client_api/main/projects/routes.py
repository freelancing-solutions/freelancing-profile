from flask import render_template, request, Blueprint, get_flashed_messages
from .. import cache
from ..library import Metatags, logged_user
from ..library.utils import const

projects_bp = Blueprint('projects', __name__, static_folder="../static", template_folder="../templates")


###########################################################################################################
# Projects Routes
@projects_bp.route('/projects', methods=['GET', 'POST'])
@logged_user
@cache.cached(timeout=const.cache_timeout_hour)
def projects(current_user: any) -> tuple:
    get_flashed_messages()
    if request.method == "GET":
        return render_template('projects.html', heading="Web Development Projects",  current_user=current_user,
                               menu_open=True, meta_tags=Metatags().set_projects()), 200
    else:
        pass


@projects_bp.route('/projects/repos/<path:path>', methods=['GET'])
@logged_user
@cache.cached(timeout=const.cache_timeout_hour)
def projects_repos(current_user: any, path: str) -> tuple:
    get_flashed_messages()
    if path == "github":
        return render_template('projects/github.html', menu_open=True, heading="Github Repositories",
                               current_user=current_user, meta_tags=Metatags().set_projects()), 200
    elif path == "codepen":
        return render_template('projects/codepen.html', menu_open=True, heading="Codepen Repositories",
                               current_user=current_user, meta_tags=Metatags().set_projects()), 200
    else:
        return render_template('projects/repos.html', menu_open=True, heading="Project Repositories",
                               current_user=current_user, meta_tags=Metatags().set_projects()), 200
