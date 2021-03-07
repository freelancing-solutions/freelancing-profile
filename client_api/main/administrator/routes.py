from flask import render_template, request, make_response, Blueprint, jsonify, current_app
from ..library import Metatags
from .. import db
from ..hireme.models import FreelanceJobModel

admin_routes = Blueprint('admin_routes', __name__)

# TODO- protect this route with login required
# and a check on the account to see if its admin account
@admin_routes.route('/admin', methods=['GET', 'POST', 'PUT', 'DELETE'])
def handle_admin():
    # TODO- check if current_user is admin user
    return render_template('/administrator/administrator.html', heading="Freelance Profile Administrator", meta_tags=Metatags().set_home())

@admin_routes.route('/admin/database/create', methods=['GET', 'POST', 'PUT', 'DELETE'])
def create_database():
    # TODO- check if current_user is admin user
    db.drop_all(app=current_app)
    db.create_all(app=current_app)
    return jsonify({"message": "Successfully created database"})

@admin_routes.route('/admin/freelance-jobs/recent', methods=['GET', 'POST', 'PUT', 'DELETE'])
def recent_freelance_jobs():
    # TODO- check if current_user is admin user
    return jsonify({'freelance_jobs': [dict(job) for job in FreelanceJobModel.query.filter_by(seen=False).all()]})

@admin_routes.route('/admin/freelance-jobs/all', methods=['GET', 'POST', 'PUT', 'DELETE'])
def all_freelance_jobs():
    # TODO- check if current_user is admin user
    return jsonify({'freelance_jobs': [dict(job) for job in FreelanceJobModel.query.filter_by().all()]})

@admin_routes.route('/admin/freelance-job', methods=['POST', 'PUT', 'DELETE'])
def freelance_jobs():
    # TODO- check if current_user is admin user
    if request.method == "POST":
        freelance_job_data = request.get_json()
        # TODO- obtain user id from current_user
        uid = ""
        project_name = freelance_job_data['project_name']
        description = freelance_job_data['description']
        print(project_name)
        print(description)
        freelance_job = FreelanceJobModel(uid=uid)

        return jsonify({'message': "freelance job successfully created"})

