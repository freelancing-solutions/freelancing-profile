
# import unittest
import uuid, time
from .. import db, create_app
from flask import current_app, url_for

def test_hireme_routes():
    """
        Testing routes for freelance jobs hireme module
    """
    from ..users.models import UserModel
    from ..library import encode_auth_token
    if not current_app:
        app = create_app()
        app.app_context().push()
    else:
        app = current_app

    app.testing = True

    with app.app_context():
        user_instances = UserModel.query.filter().all()
        if len(user_instances) > 0:
            user_instance = user_instances[0]
            token = encode_auth_token(user_instance.uid)
            test_client = app.test_client(use_cookies=True)
            test_client.allow_subdomain_redirects = True
            test_client.head(headers=[("x-access-token", token)])
        else:
            assert False, "Unable to load test cases there is no available user"

        assert test_client.get(url_for('hireme.freelancer')), "Cant access hireme freelancer"
        assert test_client.get(url_for('hireme.hire', path="freelance-jobs")), "Cant Access freelance jobs"
        assert test_client.get(url_for('hireme.hire', path="hire")), "Cant Access freelance job submission form"
        assert test_client.get(url_for('hireme.hire', path="404")), "Not properly redirected to a 404 page for inaccessible pages under hire route"
        assert test_client.get(url_for('hireme.project_details', path="xxx")), "Not able to access freelance jobs details page"
        assert test_client.get(url_for('hireme.project_details', path="")), "Not able to access freelance jobs"
        assert test_client.get(url_for('hireme.project_editor', path="")), "Not able to access freelance jobs"
        assert test_client.get(url_for('hireme.project_messages', path="xxx")), "Not able to access freelance jobs messages"
        assert test_client.get(url_for('hireme.project_messages', path="")), "project_messages unable to route to 404 page"
        assert test_client.get(url_for('hireme.project_payments', path="")), "Unable to access project Payments 404 page"
        assert test_client.get(url_for('hireme.project_payments', path="xxx")), "Unable to access project Payments page"
        # Starting to test how_to_articles_route
        assert test_client.get(url_for('hireme.how_to_articles', path='create-freelancing-account')), "Unable to access how to create freelancing account article"
        assert test_client.get(url_for('hireme.how_to_articles', path='submit-freelance-jobs')), "Unable to access how to submit-freelance-jobs article"
        assert test_client.get(url_for('hireme.how_to_articles', path='download-install-slack')), "Unable to access how to download-install-slack article"
        assert test_client.get(url_for('hireme.how_to_articles', path='download-install-teamviewer')), "Unable to access how to download-install-teamviewer article"
        assert test_client.get(url_for('hireme.how_to_articles', path='create-a-github-account')), "Unable to access how to create-a-github-account article"
        assert test_client.get(url_for('hireme.how_to_articles', path='create-a-gcp-developer-account')), "Unable to access how to create-a-gcp-developer-account article"
        assert test_client.get(url_for('hireme.how_to_articles', path='create-a-heroku-developer-account')), "Unable to access how to create-a-heroku-developer-account article"
        # Starting test cases for expectations and documentations
        assert test_client.get(url_for('hireme.expectations', path='communication-channels-procedures')), "Unable to reach communication-channels-procedures article"
        assert test_client.get(url_for('hireme.expectations', path='payments-procedures-methods')), "Unable to reach payments-procedures-methods article"
        assert test_client.get(url_for('hireme.expectations', path='due-diligence')), "Unable to reach due-diligence article"
        assert test_client.get(url_for('hireme.expectations', path='handing-over-procedures')), "Unable to reach handing-over-procedures article"
        assert test_client.get(url_for('hireme.expectations', path='maintenance-procedures')), "Unable to reach maintenance-procedures article"










