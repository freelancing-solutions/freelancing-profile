import time
from flask import render_template, request, Blueprint
from main.library import Metatags
hireme = Blueprint('hireme', __name__)


#  Temporary Data Models
temp_freelance_jobs = [
    {
        'uid': '546034t045t0459t45', # user id of the user who created the project
        'project_id': '02349u3rf3945394yr7',
        'project_name': 'Web Development',
        'project_category': 'Web Development',
        'description': 'Create a business presence website for my poultry farms it must allow order taking onsite',
        'progress': 70,
        'status': 'in-progress',
        'link_details': '02349u3rf3945394yr7',
        'time_created': time.time() * 1000, # time in milliseconds
        'est_hours_to_complete':0,   # time in milliseconds left until project is completed
        'currency' : '$',
        'budget_allocated': 500,
        'total_paid': 200
    },
    {
        'uid': '546034t5t0459t45', # user id of the user who created the project
        'project_id': '029u3rf3945394yr7',
        'project_name': 'Web Application Development',
        'project_category': 'Web Development',
        'description': 'Create a management web application for my poultry business, need to manage employees time, and etc',
        'progress': 55,
        'status': 'in-progress',
        'link_details': '02349u3rf3945394yr7',
        'time_created': time.time() * 1000, # time in milliseconds
        'est_hours_to_complete':0,   # time in milliseconds left until project is completed
        'currency' : '$',
        'budget_allocated': 500,
        'total_paid': 200
    },
    {
        'uid': '546034t5t0459t45', # user id of the user who created the project
        'project_id': '029u3rf3945394yr7',
        'project_name': 'API Development',
        'project_category': 'Back-End Development',
        'description': 'Create an API for my newsletter emailing services',
        'progress': 55,
        'status': 'in-progress',
        'link_details': '02349u3rf3945394yr7',
        'time_created': time.time() * 1000, # time in milliseconds
        'est_hours_to_complete':0,   # time in milliseconds left until project is completed
        'currency' : '$',
        'budget_allocated': 500,
        'total_paid': 200
    },
    {
        'uid': '546034t5t0459t45', # user id of the user who created the project
        'project_id': '029u3rf3945394yr7',
        'project_name': 'Rest API for react Project',
        'project_category': 'Back-End Development',
        'description': 'Create an API for my newsletter emailing services',
        'progress': 55,
        'status': 'in-progress',
        'link_details': '02349u3rf3945394yr7',
        'time_created': time.time() * 1000, # time in milliseconds
        'est_hours_to_complete':0,   # time in milliseconds left until project is completed
        'currency' : '$',
        'budget_allocated': 500,
        'total_paid': 200
    },
    {
        'uid': '546034t5t0459t45', # user id of the user who created the project
        'project_id': '029u3rf3945394yr7',
        'project_name': 'Rest API for react Project',
        'project_category': 'Back-End Development',
        'description': 'Create an API for my newsletter emailing services',
        'progress': 55,
        'status': 'in-progress',
        'link_details': '02349u3rf3945394yr7',
        'time_created': time.time() * 1000, # time in milliseconds
        'est_hours_to_complete':0,   # time in milliseconds left until project is completed
        'currency' : '$',
        'budget_allocated': 500,
        'total_paid': 200
    },
    {
        'uid': '546034t5t0459t45', # user id of the user who created the project
        'project_id': '029u3rf3945394yr7',
        'project_name': 'Rest API for react Project',
        'project_category': 'Back-End Development',
        'description': 'Create an API for my newsletter emailing services',
        'progress': 55,
        'status': 'in-progress',
        'link_details': '02349u3rf3945394yr7',
        'time_created': time.time() * 1000, # time in milliseconds
        'est_hours_to_complete':0,   # time in milliseconds left until project is completed
        'currency' : '$',
        'budget_allocated': 500,
        'total_paid': 200
    },
    {
        'uid': '546034t5t0459t45', # user id of the user who created the project
        'project_id': '029u3rf3945394yr7',
        'project_name': 'Rest API for react Project',
        'project_category': 'Back-End Development',
        'description': 'Create an API for my newsletter emailing services',
        'progress': 55,
        'status': 'in-progress',
        'link_details': '02349u3rf3945394yr7',
        'time_created': time.time() * 1000, # time in milliseconds
        'est_hours_to_complete':0,   # time in milliseconds left until project is completed
        'currency' : '$',
        'budget_allocated': 500,
        'total_paid': 200
    },
    {
        'uid': '546034t5t0459t45', # user id of the user who created the project
        'project_id': '029u3rf3945394yr7',
        'project_name': 'Rest API for react Project',
        'project_category': 'Back-End Development',
        'description': 'Create an API for my newsletter emailing services',
        'progress': 55,
        'status': 'in-progress',
        'link_details': '02349u3rf3945394yr7',
        'time_created': time.time() * 1000, # time in milliseconds
        'est_hours_to_complete':0,   # time in milliseconds left until project is completed
        'currency' : '$',
        'budget_allocated': 500,
        'total_paid': 200
    },
    {
        'uid': '546034t5t0459t45', # user id of the user who created the project
        'project_id': '029u3rf3945394yr7',
        'project_name': 'Rest API for react Project',
        'project_category': 'Back-End Development',
        'description': 'Create an API for my newsletter emailing services',
        'progress': 55,
        'status': 'in-progress',
        'link_details': '02349u3rf3945394yr7',
        'time_created': time.time() * 1000, # time in milliseconds
        'est_hours_to_complete':0,   # time in milliseconds left until project is completed
        'currency' : '$',
        'budget_allocated': 500,
        'total_paid': 200
    }
]




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
    elif path == "freelance-jobs":
        return render_template('hireme/gigs.html',
                                freelance_jobs=temp_freelance_jobs,
                                heading="My Freelance Jobs",
                                menu_open=True, 
                                meta_tags=Metatags().set_freelancer())
    elif path == "hire":
        return render_template('hireme/hire.html', heading="Submit Freelance Job",menu_open=True, meta_tags=Metatags().set_freelancer())
    else:
        return render_template('404.html', heading="Not Found",menu_open=True, meta_tags=Metatags().set_home())


@hireme.route('/hire-freelancer/freelance-job/<path:path>', methods=['GET', 'POST'])
def project_details(path):
    if path is not None:
        # TODO- search for project details using path then display results
        freelance_job = temp_freelance_jobs[3]
        # TODO- use database to select freelance job
        return render_template('hireme/project-details.html',
                                freelance_job=freelance_job,
                                heading='Freelance Job Details',
                                menu_open=True,
                                meta_tags=Metatags().set_freelancer())
    else:
        return render_template('hireme/gigs.html', heading="My Freelance Jobs",menu_open=True, meta_tags=Metatags().set_freelancer())


@hireme.route('/hire-freelancer/freelance-job-editor/<path:path>', methods=['GET', 'POST'])
def project_editor(path):
    if path is not None: # TODO- search for project details using path then display results
        freelance_job = temp_freelance_jobs[3]
        return render_template('hireme/project-editor.html', 
                                freelance_job=freelance_job,
                                heading='Freelance Job Editor',
                                menu_open=True, 
                                meta_tags=Metatags().set_freelancer())
    else:
        return render_template('404.html', heading="Not Found",menu_open=True, meta_tags=Metatags().set_home())

@hireme.route('/hire-freelancer/messages/<path:path>', methods=['GET', 'POST'])
def project_messages(path):
    if path is not None:
        project_messages = []
        return render_template('hireme/project-messages.html',
                                project_messages=project_messages,
                                job_link=path,
                                heading='Project Messages',
                                menu_open=True,
                                meta_tags=Metatags().set_project_messages())
    else:
        return render_template('404.html', heading="Not Found",menu_open=True, meta_tags=Metatags().set_home())

@hireme.route('/hire-freelancer/payments/<path:path>', methods=['GET', 'POST'])
def project_payments(path):
    if path is not None:
        # Path holds the project_id use the project_id to obtain project payment information
        project_payments = []
        return render_template('hireme/payments.html',
                                project_payments=project_payments,
                                job_link=path,
                                heading='Project Payments',
                                menu_open=True,
                                meta_tags=Metatags().set_project_payments())
    else:
        return render_template('404.html', heading="Not Found",menu_open=True, meta_tags=Metatags().set_home())


####################################################################################
# How to Articles

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
        title = "Handing Over Procedure & Production Deployment"
        return render_template('hireme/expectations/handing-over.html', heading=title, menu_open=True, meta_tags=Metatags().set_handinqover())
    elif path == "maintenance-procedures":
        title = "Maintenance Procedures & Agreements"
        return render_template('hireme/expectations/maintenance.html', heading=title, menu_open=True, meta_tags=Metatags().set_maintenance())
    else:
        pass
