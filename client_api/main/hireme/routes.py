from flask import render_template, request, Blueprint
from main.library import Metatags
hireme = Blueprint('hireme', __name__)


###########################################################################################################
# Freelance and Hire Routes
@hireme.route('/hire-freelancer', methods=['GET', 'POST'])
def freelancer():
    if request.method == "GET":
        return render_template('hireme.html', heading="Hiring a Freelancer", menu_open=True, meta_tags=Metatags().set_freelancer())
    else:
        pass


@hireme.route('/hire-freelancer/<path:path>', methods=['GET', 'POST'])
def hire(path):
    if path == 'login':
        return render_template('hireme/login.html', heading="Login",menu_open=True, meta_tags=Metatags().set_freelancer())
    elif path == "gigs":
        return render_template('hireme/gigs.html', heading="My Previous Gigs",menu_open=True, meta_tags=Metatags().set_freelancer())
    elif path == "hire":
        return render_template('hireme/hire.html', heading="Hire a Freelancer",menu_open=True, meta_tags=Metatags().set_freelancer())
    else:
        return render_template('404.html', heading="Not Found",menu_open=True, meta_tags=Metatags().set_home())


@hireme.route('/hire-freelancer/gigs/<path:path>', methods=['GET', 'POST'])
def project_details(path):
    if path is not None:
        # TODO- search for project details using path then display results
        return render_template('hireme/project-details.html', heading='Project Details',menu_open=True,meta_tags=Metatags().set_freelancer())
    else:
        return render_template('hireme/gigs.html', heading="My Previous Gigs",menu_open=True, meta_tags=Metatags().set_freelancer())


@hireme.route('/hire-freelancer/gig-editor/<path:path>', methods=['GET', 'POST'])
def project_editor(path):
    if path is not None: # TODO- search for project details using path then display results
        return render_template('hireme/project-editor.html', heading='Project Editor',menu_open=True, meta_tags=Metatags().set_freelancer())
    else:
        return render_template('404.html', heading="Not Found",menu_open=True, meta_tags=Metatags().set_home())


@hireme.route('/hire-freelancer/how-to/<path:path>', methods=['GET'])
def how_to_articles(path):
    """
        How to articles on hiring a freelancer
    """

    if path == "create-freelancing-account":
        title = "How to create a freelancing account"
        return render_template('hireme/howto/create-freelancing-account.html', heading=title,menu_open=True, meta_tags=Metatags().set_how_to_create_freelancing_account())
    elif path == "submit-freelance-jobs":
        title="How to Submit Freelance Jobs"
        return render_template('hireme/howto/submit-freelance-job.html', heading=title,menu_open=True, meta_tags=Metatags().set_submit_freelance_jobs())
    elif path == "download-install-slack":
        title ="How to download and Install Slack"
        return render_template('hireme/howto/download-install-slack.html', heading=title,menu_open=True, meta_tags=Metatags().set_download_slack())
    elif path == "download-install-teamviewer":
        title ="How to download and Install Teamviewer"
        return render_template('hireme/howto/download-install-teamviewer.html', heading=title,menu_open=True, meta_tags=Metatags().set_download_teamviewer())

    elif path == "create-a-github-account":
        title ="Create a Github account"
        return render_template('hireme/howto/create-github-account.html', heading=title,menu_open=True, meta_tags=Metatags().set_create_github())
    elif path == "create-a-gcp-developer-account":
        title ="Create a GCP Developer Account"
        return render_template('hireme/howto/register-gcp-account.html', heading=title,menu_open=True, meta_tags=Metatags().set_gcp_account())
    elif path == "create-a-heroku-developer-account":
        title ="Create a Heroku Developer Account"
        return render_template('hireme/howto/create-heroku-account.html', heading=title,menu_open=True, meta_tags=Metatags().set_heroku_account())
    else:
        pass


@hireme.route('/hire-freelancer/expectations/<path:path>', methods=['GET'])
def expectations(path):
    """
        Things expected from each client during and on completion of freelance jobs
    """
    if path == "communication-channels-procedures":
        title = "Communication Channels and Procedures"
        return render_template('hireme/expectations/communication.html', heading=title, menu_open=True, meta_tags=Metatags().set_communications())
    elif path == "payments-procedures-methods":
        title = "Payments Procedures and Methods"
        return render_template('hireme/expectations/payments.html', heading=title, menu_open=True, meta_tags=Metatags().set_payments())
    elif path == "due-diligence":
        title = "Due Diligence and Legal Expectations"
        return render_template('hireme/expectations/diligence.html', heading=title, menu_open=True, meta_tags=Metatags().set_diligence())
    elif path == "handing-over-procedures":
        title = "handing Over Procedure & Production Deployment"
        return render_template('hireme/expectations/handing-over.html', heading=title, menu_open=True, meta_tags=Metatags().set_handinqover())
    elif path == "maintenance-procedures":
        title = "Maintenance Procedures & Agreements"
        return render_template('hireme/expectations/maintenance.html', heading=title, menu_open=True, meta_tags=Metatags().set_maintenance())
    else:
        pass
