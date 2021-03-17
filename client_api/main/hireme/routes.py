import time
from flask import render_template, request, Blueprint,flash,get_flashed_messages
from ..library import Metatags, token_required, logged_user
from .models import FreelanceJobModel
hireme = Blueprint('hireme', __name__, static_folder="static", template_folder="templates")

#  Temporary Data Models
temp_freelance_jobs = []

# Routes Mappings
path_routes = {
    'freelancer': '/hire-freelancer',
    'hire': '/hire-freelancer/<path:path>',
    'project_details' : '/hire-freelancer/freelance-job<path:path>',
    'project_editor' : '/hire-freelancer/freelance-job-editor/<path:path>',
    'project_messages' : '/hire-freelancer/messages/<path:path>',
    'project_payments' : '/hire-freelancer/payments/<path:path>',
    'how_to_articles' : '/freelance-articles/how-to/<path:path>',
    'expectations' : '/freelance-articles/expectations/<path:path>'
}

expect_paths = {
    'communication':'communication-channels-procedures',
    'payments':'payments-procedures-methods',
    'due-diligence':'due-diligence',
    'handingover':'handing-over-procedures',
    'maintenance':'maintenance-procedures'
}
###########################################################################################################
# Freelance and Hire Routes
@hireme.route(path_routes['freelancer'], methods=['GET'])
@logged_user
def freelancer(current_user):
    get_flashed_messages()
    if request.method == "GET":
        return render_template('hireme.html', heading="Hiring a Freelancer", current_user=current_user,
        menu_open=True, meta_tags=Metatags().set_freelancer())

@hireme.route(path_routes['hire'], methods=['GET', 'POST'])
@token_required
def hire(current_user,path):
    get_flashed_messages()
    print("Current User", current_user)
    if (path == "freelance-jobs") and current_user:
        freelance_jobs = FreelanceJobModel.query.filter_by(_uid=current_user.uid).all()
        return render_template('hireme/gigs.html',
                                freelance_jobs=freelance_jobs,
                                heading="My Freelance Jobs",
                                menu_open=True,
                                current_user=current_user,
                                meta_tags=Metatags().set_freelancer())
    elif path == "hire":
        return render_template('hireme/hire.html', heading="Submit Freelance Job",current_user=current_user,
        menu_open=True, meta_tags=Metatags().set_freelancer())
    else:
        return render_template('404.html', heading="Not Found",menu_open=True,current_user=current_user,
         meta_tags=Metatags().set_home())

@hireme.route(path_routes['project_details'], methods=['GET', 'POST'])
@token_required
def project_details(current_user,path):
    get_flashed_messages()
    if path is not None:
        freelance_job = FreelanceJobModel.query.filter_by(_project_id=path).first()
        if freelance_job:
            return render_template('hireme/project-details.html',
                                    freelance_job=freelance_job,
                                    heading='Freelance Job Details',
                                    menu_open=True,
                                    current_user=current_user,
                                    meta_tags=Metatags().set_freelancer())
        else:
            return render_template('404.html', heading="Not Found",menu_open=True,
             current_user=current_user,meta_tags=Metatags().set_home())
    else:
        return render_template('hireme/gigs.html', heading="My Freelance Jobs",menu_open=True, 
        current_user=current_user,meta_tags=Metatags().set_freelancer())

@hireme.route(path_routes['project_messages'], methods=['GET', 'POST'])
@token_required
def project_editor(current_user,path):
    get_flashed_messages()
    if path is not None:
        freelance_job = FreelanceJobModel.query.filter_by(_project_id=path).first()
        return render_template('hireme/project-editor.html',
                                freelance_job=freelance_job,
                                heading='Freelance Job Editor',
                                menu_open=True,
                                current_user=current_user,
                                meta_tags=Metatags().set_freelancer())
    else:
        return render_template('404.html', heading="Not Found",menu_open=True,
        current_user=current_user, meta_tags=Metatags().set_home())

@hireme.route(path_routes['project_payments'], methods=['GET', 'POST'])
@token_required
def project_messages(current_user,path):
    get_flashed_messages()
    if path is not None:
        project_messages = []
        return render_template('hireme/project-messages.html',
                                project_messages=project_messages,
                                job_link=path,
                                heading='Project Messages',
                                menu_open=True,
                                current_user=current_user,
                                meta_tags=Metatags().set_project_messages())
    else:
        return render_template('404.html', heading="Not Found",menu_open=True,
        current_user=current_user, meta_tags=Metatags().set_home())

@hireme.route(path_routes['project_payments'], methods=['GET', 'POST'])
@token_required
def project_payments(current_user,path):
    get_flashed_messages()
    if path is not None:
        # Path holds the project_id use the project_id to obtain project payment information
        project_payments = []
        return render_template('hireme/payments.html',
                                project_payments=project_payments,
                                job_link=path,
                                heading='Project Payments',
                                menu_open=True,
                                current_user=current_user,
                                meta_tags=Metatags().set_project_payments())
    else:
        return render_template('404.html', heading="Not Found",menu_open=True,
        current_user=current_user, meta_tags=Metatags().set_home())

####################################################################################
# How to Articles

@hireme.route(path_routes['how_to_articles'], methods=['GET'])
@logged_user
def how_to_articles(current_user,path):
    get_flashed_messages()
    """
        How to articles on hiring a freelancer
    """
    if path == "create-freelancing-account":
        title = "How to create a freelancing account"
        return render_template('hireme/howto/create-freelancing-account.html', heading=title,menu_open=True,
        current_user=current_user,meta_tags=Metatags().set_how_to_create_freelancing_account())
    elif path == "submit-freelance-jobs":
        title="How to Submit Freelance Jobs"
        return render_template('hireme/howto/submit-freelance-job.html', heading=title,menu_open=True,
        current_user=current_user,meta_tags=Metatags().set_submit_freelance_jobs())
    elif path == "download-install-slack":
        title ="How to download and Install Slack"
        return render_template('hireme/howto/download-install-slack.html', heading=title,menu_open=True,
        current_user=current_user,meta_tags=Metatags().set_download_slack())
    elif path == "download-install-teamviewer":
        title ="How to download and Install Teamviewer"
        return render_template('hireme/howto/download-install-teamviewer.html', heading=title,menu_open=True,
        current_user=current_user,meta_tags=Metatags().set_download_teamviewer())
    elif path == "create-a-github-account":
        title ="Create a Github account"
        return render_template('hireme/howto/create-github-account.html', heading=title,menu_open=True,
        current_user=current_user,meta_tags=Metatags().set_create_github())
    elif path == "create-a-gcp-developer-account":
        title ="Create a GCP Developer Account"
        return render_template('hireme/howto/register-gcp-account.html', heading=title,menu_open=True,
        current_user=current_user,meta_tags=Metatags().set_gcp_account())
    elif path == "create-a-heroku-developer-account":
        title ="Create a Heroku Developer Account"
        return render_template('hireme/howto/create-heroku-account.html', heading=title,menu_open=True,
        current_user=current_user,meta_tags=Metatags().set_heroku_account())
    else:
        return render_template('404.html', heading="Not Found",menu_open=True,
        current_user=current_user,meta_tags=Metatags().set_home())


@hireme.route(path_routes['expectations'], methods=['GET'])
@logged_user
def expectations(current_user,path):
    get_flashed_messages()
    """
        Things expected from each client during and on completion of freelance jobs
    """
    if path == expect_paths['communication']:
        title = "Communication Channels and Procedures"
        return render_template('hireme/expectations/communication.html', heading=title, menu_open=True,
        current_user=current_user,meta_tags=Metatags().set_communications())
    elif path == expect_paths['payments']:
        title = "Payments Procedures and Methods"
        return render_template('hireme/expectations/payments.html', heading=title, menu_open=True,
        current_user=current_user,meta_tags=Metatags().set_payments())
    elif path == expect_paths['due-diligence']:
        title = "Due Diligence and Legal Expectations"
        return render_template('hireme/expectations/diligence.html', heading=title, menu_open=True,
        current_user=current_user,meta_tags=Metatags().set_diligence())
    elif path == expect_paths['handingover']:
        title = "Handing Over Procedure & Production Deployment"
        return render_template('hireme/expectations/handing-over.html', heading=title, menu_open=True,
        current_user=current_user,meta_tags=Metatags().set_handinqover())
    elif path == expect_paths['maintenance']:
        title = "Maintenance Procedures & Agreements"
        return render_template('hireme/expectations/maintenance.html', heading=title, menu_open=True,
        current_user=current_user,meta_tags=Metatags().set_maintenance())
    else:
        return render_template('404.html', heading="Not Found",menu_open=True,
        current_user=current_user,meta_tags=Metatags().set_home())