
Justice Ndou Web Development and Freelance Profile
-
***The Purpose of this website is to showcase my skills in***

- Development Time
  
  [![wakatime](https://wakatime.com/badge/github/freelancing-solutions/freelancing-profile.svg)](https://wakatime.com/badge/github/freelancing-solutions/freelancing-profile)

- Front End Web Development

      - Vanilla Javascript
      - Handlebars Templates
      - React.js
      - Jinja2
      - HTML5
      - CSS
      - BootStrap
      - Common E-Commerce, Payments API Integration (e.g PayPal)

- Back End Web Development

        - Python 3.x
            - Flask
            - Flask_restful
            - FastApi
            - Jinja2
            - Common E-Commerce, Payments API Integration (e.g PayPal)

        - Node.js
            - Express.js Framework
            - Feathers.io
            - Sockets.io
            - Firebase Functions (Node.js)
            - GCP Functions (Node.js)
            - Cloud Run (Node.js)

- How this Web Application / Website was created:

        - Python
        - Flask
        - Flask_restful
        - Flask SQLAlchemy
        - MySQL
        - Jinja Templates
        - Handlebars Templates
        - Javascript
        - BootStrap
        - JWT Basic Auth , Token Based Authentication

- Upcoming Features

        - React Admin
            - (For Administration Tasks)

- Developer

      - Name : [Justice Ndou](https://justice-ndou.site)
      - Email : mobiusndou@gmail.com
      - Twitter : [Twitter Profile](https://twitter.com/blueitserver)

- Work In Progress
      - it didnt take me a week before i realize i could have done this better

```python
import time
from flask import render_template, request, Blueprint, get_flashed_messages, jsonify, redirect, url_for
from sqlalchemy.exc import OperationalError, DisconnectionError, InvalidRequestError

from .. import db, cache
from ..library import Metatags, token_required, logged_user
from .models import FreelanceJobModel, ProjectMessages
from ..library.utils import const
from ..payments.models import PaymentModel, TransactionModel

hireme = Blueprint('hireme', __name__, static_folder="static", template_folder="templates")

#  Temporary Data Models
temp_freelance_jobs: list = []

# Routes Mappings
path_routes: dict = {
    'freelancer': '/hire-freelancer',
    'hire': '/hire-freelancer/<path:path>',
    'project_details': '/projects/freelance-job/<path:path>',
    'project_editor': '/projects/freelance-job-editor/<path:path>',
    'project_messages': '/projects/messages/<path:path>',
    'project_payments': '/projects/payments/<path:path>',
    'how_to_articles': '/freelance-articles/how-to/<path:path>',
    'expectations': '/freelance-articles/expectations/<path:path>'
}

expect_paths: dict = {
    'communication': 'communication-channels-procedures',
    'payments': 'payments-procedures-methods',
    'due-diligence': 'due-diligence',
    'handingover': 'handing-over-procedures',
    'maintenance': 'maintenance-procedures'
}


###########################################################################################################
# Freelance and Hire Routes
@hireme.route(path_routes['freelancer'], methods=['GET'])
@logged_user
@cache.cached(timeout=const.cache_timeout_hour)
def freelancer(current_user: any) -> tuple:
    get_flashed_messages()
    if request.method == "GET":
        return render_template('hireme.html', heading="Hiring a Freelancer", current_user=current_user,
                               menu_open=True, meta_tags=Metatags().set_freelancer()), 200


@hireme.route(path_routes['hire'], methods=['GET', 'POST'])
@token_required
def hire(current_user: any, path: str) -> tuple:
    get_flashed_messages()
    if request.method == "GET":
        if current_user and current_user.uid:
            if path == "freelance-jobs":
                try:
                    freelance_jobs = FreelanceJobModel.query.filter_by(_uid=current_user.uid).all()
                except OperationalError as e:
                    return render_template('error.html', heading='Database Error',
                                           message='Database error',
                                           meta_tags=Metatags().set_home()), 500
                except DisconnectionError as e:
                    return render_template('error.html', heading='Database Error',
                                           message='Database Connection Error',
                                           meta_tags=Metatags().set_home()), 500

                return render_template('hireme/gigs.html',
                                       freelance_jobs=freelance_jobs,
                                       heading="My Freelance Jobs",
                                       menu_open=True,
                                       current_user=current_user,
                                       meta_tags=Metatags().set_freelancer()), 200
            elif path == "hire":
                return render_template('hireme/hire.html', heading="Submit Freelance Job", current_user=current_user,
                                       menu_open=True, meta_tags=Metatags().set_freelancer()), 200
            else:
                return render_template('404.html', heading="Not Found", menu_open=True, current_user=current_user,
                                       meta_tags=Metatags().set_home()), 404
        else:
            return render_template('error.html', heading="Not Authorized", menu_open=True,
                                   message="Could not determine Current User Please login",
                                   code=401,
                                   current_user=current_user, meta_tags=Metatags().set_home()), 401
    elif request.method == "POST":
        if current_user and current_user.uid:
            job_details: dict = request.get_json()

            if 'project_name' in job_details and not(job_details['project_name'] == ""):
                project_name: str = job_details['project_name']
            else:
                return jsonify({'status': "failure", 'message:': "project name is required"}), 404

            if 'description' in job_details and not(job_details['description'] == ""):
                description: str = job_details['description']
            else:
                return jsonify({'status': "failure", 'message:': "description is required"}), 404

            if ('budget' in job_details) and not(job_details['budget'] == ""):
                budget: int = int(job_details['budget'])
            else:
                return jsonify({'status': "failure", 'message:': "budget is required"}), 404

            if 'currency' in job_details and not(job_details['currency'] == ""):
                currency: str = job_details['currency']
            else:
                return jsonify({'status': "failure", 'message:': "currency is required"}), 404

            if 'est_duration' in job_details and not(job_details['est_duration'] == ""):
                est_duration: int = int(job_details['est_duration'])
            else:
                return jsonify({'status': "failure", 'message:': "project duration is required"}), 404

            try:
                freelance_job: FreelanceJobModel = FreelanceJobModel(uid=current_user.uid,
                                                                     project_name=project_name,
                                                                     description=description,
                                                                     est_hours_to_complete=est_duration,
                                                                     currency=currency,
                                                                     budget_allocated=budget)

                message: str = """ Welcome to my freelance portfolio - if you needed me to know about anything related 
                to this project please use this messaging board"""

                freelance_job.add_payment(payment=PaymentModel(uid=current_user.uid,
                                                               project_id=freelance_job.project_id,
                                                               amount=budget, currency=currency))
                freelance_job.add_message(message=ProjectMessages(uid=current_user.uid,
                                                                  project_id=freelance_job.project_id,
                                                                  message=message))
                message: str = """Read through the setup instructions on the hire me page"""
                freelance_job.add_message(message=ProjectMessages(uid=current_user.uid,
                                                                  project_id=freelance_job.project_id,
                                                                  message=message))
                db.session.add(freelance_job)
                db.session.commit()
                return jsonify({'status': "success", 'message': "successfully created your freelance job",
                                "project_id": freelance_job.project_id})
            except OperationalError as e:
                db.session.rollback()
                db.session.commit()
                message: str = "Database Error creating freelance job"
                return jsonify({'status': "failure", 'message:': message}), 500
            except DisconnectionError as e:
                db.session.rollback()
                db.session.commit()
                message: str = "Database Error Unable to connect to database"
                return jsonify({'status': "failure", 'message:': message}), 500
            except InvalidRequestError as e:
                db.session.rollback()
                db.session.commit()
                message: str = "Database Error Unable to transact with database"
                return jsonify({'status': "failure", 'message:': message}), 500

        return redirect(url_for('users.login')), 404


@hireme.route(path_routes['project_details'], methods=['GET', 'POST'])
@token_required
def project_details(current_user: any, path: str) -> tuple:
    get_flashed_messages()
    print('down first')
    if not(path is None) and not(path == ""):
        try:
            freelance_job: FreelanceJobModel = FreelanceJobModel.query.filter_by(_project_id=path).first()
        except OperationalError as e:
            return render_template('error.html', heading='Database Error', message='error connecting to database',
                                   meta_tags=Metatags().set_home()), 500
        except DisconnectionError as e:
            message: str = "Database Error Unable to connect to database"
            return jsonify({'status': "failure", 'message:': message}), 500

        if freelance_job and freelance_job.project_id:
            return render_template('hireme/project-details.html',
                                   freelance_job=freelance_job,
                                   heading='Freelance Job Details',
                                   menu_open=True,
                                   current_user=current_user,
                                   meta_tags=Metatags().set_freelancer()), 200
        else:
            return render_template('404.html', heading="Not Found", menu_open=True,
                                   current_user=current_user, meta_tags=Metatags().set_home()), 404
    else:
        return render_template('hireme/gigs.html', heading="My Freelance Jobs", menu_open=True,
                               current_user=current_user, meta_tags=Metatags().set_freelancer()), 200


@hireme.route(path_routes['project_editor'], methods=['GET', 'POST'])
@token_required
def project_editor(current_user: any, path: str) -> tuple:
    get_flashed_messages()
    if not(path is None) and not(path == ""):
        try:
            freelance_job: FreelanceJobModel = FreelanceJobModel.query.filter_by(_project_id=path).first()
        except OperationalError as e:
            return render_template('error.html', heading='Database Error', message='error connecting to database',
                                   meta_tags=Metatags().set_home()), 500
        except DisconnectionError as e:
            message: str = "Database Error Unable to connect to database"
            return render_template('error.html', heading='Database Error', message=message,
                                   meta_tags=Metatags().set_home()), 500

        if freelance_job and freelance_job.project_id:
            return render_template('hireme/project-editor.html',
                                   freelance_job=freelance_job,
                                   heading='Freelance Job Editor',
                                   menu_open=True,
                                   current_user=current_user,
                                   meta_tags=Metatags().set_freelancer()), 200
        else:
            return render_template('404.html', heading="Not Found", menu_open=True,
                                   current_user=current_user, meta_tags=Metatags().set_home()), 404

    else:
        return render_template('404.html', heading="Not Found", menu_open=True,
                               current_user=current_user, meta_tags=Metatags().set_home()), 404


@hireme.route(path_routes['project_messages'], methods=['GET', 'POST'])
@token_required
def project_messages(current_user: any, path: str) -> tuple:
    get_flashed_messages()
    if not(path is None) and not(path == ""):
        try:
            project_messages_list: list = ProjectMessages.query.filter_by(_project_id=path).all()
        except OperationalError as e:
            message: str = "Database Error creating project messages"
            return render_template('404.html', heading="Database Error", menu_open=True,
                                   message=message, current_user=current_user,
                                   meta_tags=Metatags().set_home()), 404
        except DisconnectionError as e:
            message: str = "Error connecting to database"
            return render_template('404.html', heading="Database Error", menu_open=True,
                                   message=message, current_user=current_user,
                                   meta_tags=Metatags().set_home()), 404

        return render_template('hireme/project-messages.html',
                               project_messages=project_messages_list,
                               job_link=path,
                               heading='Project Messages',
                               menu_open=True,
                               current_user=current_user,
                               meta_tags=Metatags().set_project_messages()), 200
    else:
        return render_template('404.html', heading="Not Found", menu_open=True,
                               current_user=current_user, meta_tags=Metatags().set_home()), 404


@hireme.route(path_routes['project_payments'], methods=['GET', 'POST'])
@token_required
def project_payments(current_user: any, path: str) -> tuple:
    get_flashed_messages()
    if current_user and current_user.uid:
        if not(path is None) and not(path == ""):
            # Path holds the project_id use the project_id to obtain project payment information
            try:
                project_payment = PaymentModel.query.filter_by(_project_id=path).first()
            except OperationalError as e:
                return render_template('error.html', heading='Database Error', message='error connecting to database',
                                       meta_tags=Metatags().set_home()), 500
            except DisconnectionError as e:
                message: str = "Error connecting to database"
                return render_template('404.html', heading="Database Error", menu_open=True,
                                       message=message, current_user=current_user,
                                       meta_tags=Metatags().set_home()), 404

            if project_payment and project_payment.payment_id:
                try:
                    transactions_list: list = TransactionModel.query.filter_by(
                        _payment_id=project_payment.payment_id).all()

                except OperationalError as e:
                    return render_template('error.html', heading='Database Error',
                                           message='error connecting to database',
                                           meta_tags=Metatags().set_home()), 500

                except DisconnectionError as e:
                    message: str = "Error connecting to database"
                    return render_template('404.html', heading="Database Error", menu_open=True,
                                           message=message, current_user=current_user,
                                           meta_tags=Metatags().set_home()), 404

                return render_template('hireme/payments.html',
                                       project_payment=project_payment,
                                       transactions_list=transactions_list,
                                       job_link=path,
                                       heading='Project Payments',
                                       menu_open=True,
                                       current_user=current_user,
                                       meta_tags=Metatags().set_project_payments()), 200
            else:
                return render_template('404.html', heading="Not Found", menu_open=True,
                                       current_user=current_user, meta_tags=Metatags().set_home()), 404
        else:
            return render_template('404.html', heading="Not Found", menu_open=True,
                                   current_user=current_user, meta_tags=Metatags().set_home()), 404
    else:
        return render_template('error.html', heading="Not Authorized", menu_open=True,
                               current_user=current_user, meta_tags=Metatags().set_home()), 401


####################################################################################
# How to Articles

@hireme.route(path_routes['how_to_articles'], methods=['GET'])
@logged_user
@cache.cached(timeout=const.cache_timeout_hour)
def how_to_articles(current_user: any, path: str) -> tuple:
    get_flashed_messages()
    """
        How to articles on hiring a freelancer
    """
    if path == "create-freelancing-account":
        title: str = "How to create a freelancing account"
        return render_template('hireme/howto/create-freelancing-account.html', heading=title, menu_open=True,
                               current_user=current_user,
                               meta_tags=Metatags().set_how_to_create_freelancing_account()), 200

    elif path == "submit-freelance-jobs":
        title: str = "How to Submit Freelance Jobs"
        return render_template('hireme/howto/submit-freelance-job.html', heading=title, menu_open=True,
                               current_user=current_user, meta_tags=Metatags().set_submit_freelance_jobs()), 200

    elif path == "download-install-slack":
        title: str = "How to download and Install Slack"
        return render_template('hireme/howto/download-install-slack.html', heading=title, menu_open=True,
                               current_user=current_user, meta_tags=Metatags().set_download_slack()), 200

    elif path == "download-install-teamviewer":
        title: str = "How to download and Install Teamviewer"
        return render_template('hireme/howto/download-install-teamviewer.html', heading=title, menu_open=True,
                               current_user=current_user, meta_tags=Metatags().set_download_teamviewer()), 200

    elif path == "create-a-github-account":
        title: str = "Create a Github account"
        return render_template('hireme/howto/create-github-account.html', heading=title, menu_open=True,
                               current_user=current_user, meta_tags=Metatags().set_create_github()), 200

    elif path == "create-a-gcp-developer-account":
        title: str = "Create a GCP Developer Account"
        return render_template('hireme/howto/register-gcp-account.html', heading=title, menu_open=True,
                               current_user=current_user, meta_tags=Metatags().set_gcp_account()), 200

    elif path == "create-a-heroku-developer-account":
        title: str = "Create a Heroku Developer Account"
        return render_template('hireme/howto/create-heroku-account.html', heading=title, menu_open=True,
                               current_user=current_user, meta_tags=Metatags().set_heroku_account()), 200
    else:
        return render_template('404.html', heading="Not Found", menu_open=True,
                               current_user=current_user, meta_tags=Metatags().set_home()), 404


@hireme.route(path_routes['expectations'], methods=['GET'])
@logged_user
@cache.cached(timeout=const.cache_timeout_hour)
def expectations(current_user: any, path: str) -> tuple:
    get_flashed_messages()
    """
        Things expected from each client during and on completion of freelance jobs
    """
    if path == expect_paths['communication']:
        title: str = "Communication Channels and Procedures"
        return render_template('hireme/expectations/communication.html', heading=title, menu_open=True,
                               current_user=current_user, meta_tags=Metatags().set_communications()), 200

    elif path == expect_paths['payments']:
        title: str = "Payments Procedures and Methods"
        return render_template('hireme/expectations/payments.html', heading=title, menu_open=True,
                               current_user=current_user, meta_tags=Metatags().set_payments()), 200

    elif path == expect_paths['due-diligence']:
        title: str = "Due Diligence and Legal Expectations"
        return render_template('hireme/expectations/diligence.html', heading=title, menu_open=True,
                               current_user=current_user, meta_tags=Metatags().set_diligence()), 200

    elif path == expect_paths['handingover']:
        title: str = "Handing Over Procedure & Production Deployment"
        return render_template('hireme/expectations/handing-over.html', heading=title, menu_open=True,
                               current_user=current_user, meta_tags=Metatags().set_handinqover()), 200

    elif path == expect_paths['maintenance']:
        title: str = "Maintenance Procedures & Agreements"
        return render_template('hireme/expectations/maintenance.html', heading=title, menu_open=True,
                               current_user=current_user, meta_tags=Metatags().set_maintenance()), 200

    else:
        return render_template('404.html', heading="Not Found", menu_open=True,
                               current_user=current_user, meta_tags=Metatags().set_home()), 404      
```
