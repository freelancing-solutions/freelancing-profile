from flask import render_template, request, Blueprint
from client_api.main import Metatags
hireme = Blueprint('hireme', __name__)


###########################################################################################################
# Freelance and Hire Routes
@hireme.route('/hire-freelancer', methods=['GET', 'POST'])
def freelancer():
    if request.method == "GET":
        return render_template('hireme.html', heading="Hiring a Freelancer", meta_tags=Metatags().set_freelancer())
    else:
        pass


@hireme.route('/hire-freelancer/<path:path>', methods=['GET', 'POST'])
def hire(path):
    if path == 'login':
        return render_template('hireme/login.html', heading="Login", meta_tags=Metatags().set_freelancer())
    elif path == "gigs":
        return render_template('hireme/gigs.html', heading="My Previous Gigs", meta_tags=Metatags().set_freelancer())
    elif path == "hire":
        return render_template('hireme/hire.html', heading="Hire a Freelancer", meta_tags=Metatags().set_freelancer())
    else:
        return render_template('404.html', heading="Not Found", meta_tags=Metatags().set_home())


@hireme.route('/hire-freelancer/gigs/<path:path>', methods=['GET', 'POST'])
def project_details(path):
    if path is not None:
        # TODO- search for project details using path then display results
        return render_template('hireme/project-details.html', heading='Project Details', meta_tags=Metatags().set_freelancer())
    else:
        return render_template('hireme/gigs.html', heading="My Previous Gigs", meta_tags=Metatags().set_freelancer())


@hireme.route('/hire-freelancer/gig-editor/<path:path>', methods=['GET', 'POST'])
def project_editor(path):
    if path is not None: # TODO- search for project details using path then display results
        return render_template('hireme/project-editor.html', heading='Project Editor', meta_tags=Metatags().set_freelancer())
    else:
        return render_template('404.html', heading="Not Found", meta_tags=Metatags().set_home())

