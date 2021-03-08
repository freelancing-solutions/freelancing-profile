from flask import render_template, request, Blueprint,flash,get_flashed_messages
from ..library import Metatags, logged_user
projects_bp = Blueprint('projects', __name__)

###########################################################################################################
# Projects Routes
@projects_bp.route('/projects', methods=['GET', 'POST'])
@logged_user
def projects(current_user):
    get_flashed_messages()
    if request.method == "GET":
        return render_template('projects.html', heading="Web Development Projects",current_user=current_user,
                                menu_open=True, meta_tags=Metatags().set_projects())
    else:
        pass

@projects_bp.route('/projects/repos/<path:path>', methods=['GET'])
@logged_user
def projects_repos(current_user,path):
    get_flashed_messages()
    if path == "github":
        return render_template('projects/github.html',menu_open=True, heading="Github Repositories",
                               current_user=current_user,meta_tags=Metatags().set_projects())
    elif path == "codepen":
        return render_template('projects/codepen.html',menu_open=True, heading="Codepen Repositories",
                               current_user=current_user,meta_tags=Metatags().set_projects())
    else:
        return render_template('projects/repos.html',menu_open=True, heading="Project Repositories",
                               current_user=current_user,meta_tags=Metatags().set_projects())