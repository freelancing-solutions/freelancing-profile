from flask import render_template, request, Blueprint
from main.library import Metatags

projects_bp = Blueprint('projects', __name__)


###########################################################################################################
# Projects Routes
@projects_bp.route('/projects', methods=['GET', 'POST'])
def projects():
    if request.method == "GET":
        return render_template('projects.html', heading="Web Development Projects",menu_open=True, meta_tags=Metatags().set_projects())
    else:
        pass

@projects_bp.route('/projects/repos/<path:path>', methods=['GET'])
def projects_repos(path):
    if path == "github":
        return render_template('projects/github.html',menu_open=True, heading="Github Repositories",
                               meta_tags=Metatags().set_projects())
    elif path == "codepen":
        return render_template('projects/codepen.html',menu_open=True, heading="Codepen Repositories",
                               meta_tags=Metatags().set_projects())
    else:
        return render_template('projects/repos.html',menu_open=True, heading="Project Repositories",
                               meta_tags=Metatags().set_projects())

