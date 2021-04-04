from flask import (render_template, request, make_response, Blueprint, jsonify,
                   current_app, flash, get_flashed_messages)
from sqlalchemy.exc import OperationalError

from ..library import Metatags, token_required
from .. import db
from ..hireme.models import FreelanceJobModel
from ..main.models import ContactModel


admin_routes = Blueprint('admin_routes', __name__, static_folder="../static", template_folder="../templates")


# TODO- protect this route with login required
# and a check on the account to see if its admin account
@admin_routes.route('/admin', methods=['GET', 'POST', 'PUT', 'DELETE'])
@token_required
def handle_admin(current_user: any) -> any:
    get_flashed_messages()
    if current_user and current_user.admin:
        title: str = "Freelance Profile Administrator"
        return render_template('administrator/administrator.html', heading=title,
                               current_user=current_user, menu_open=True, meta_tags=Metatags().set_home()), 200
    else:
        return jsonify({'message': 'you are not authorized to use this resource'}), 401


@admin_routes.route('/admin/database/create', methods=['GET', 'POST', 'PUT', 'DELETE'])
@token_required
def create_database(current_user) -> any:
    get_flashed_messages()
    # TODO- check if current_user is admin user
    if current_user and current_user.admin:
        try:
            db.drop_all(app=current_app)
            db.create_all(app=current_app)
        except OperationalError as e:
            return jsonify({"message": "database error"}), 500
        return jsonify({"message": "Successfully created database"}), 200
    else:
        return jsonify({"message": "You are not authorized to execute this command"}), 401


@admin_routes.route('/admin/freelance-jobs/recent', methods=['GET', 'POST', 'PUT', 'DELETE'])
@token_required
def recent_freelance_jobs(current_user: any) -> any:
    get_flashed_messages()
    # TODO- check if current_user is admin user
    if current_user and current_user.admin:
        try:
            return jsonify({'freelance_jobs': [dict(job) for job in FreelanceJobModel.query.filter_by(seen=False).all()],
                            'message': 'you have successfully fetched recent freelance jobs'}), 200
        except OperationalError as e:
            return jsonify({"status": "failure", "message": "database error"}), 500
    else:
        return jsonify({'message': 'you are not authorized to use this resource'}), 401


@admin_routes.route('/admin/freelance-jobs/all', methods=['GET', 'POST', 'PUT', 'DELETE'])
@token_required
def all_freelance_jobs(current_user: any) -> any:
    get_flashed_messages()
    # TODO- check if current_user is admin user
    if current_user and current_user.admin:
        try:
            return jsonify({'freelance_jobs': [dict(job) for job in FreelanceJobModel.query.filter_by().all()],
                            'message': 'you have successfully retrieved all freelance jobs'}), 200
        except OperationalError as e:
            return jsonify({"status": "failure", "message": "database error"}), 500
    else:
        return jsonify({'message':"you are not authorized to use this resource"}), 401


@admin_routes.route('/admin/freelance-job', methods=['POST', 'PUT', 'DELETE'])
@token_required
def freelance_jobs(current_user: any) -> any:
    get_flashed_messages()
    # TODO- check if current_user is admin user
    if current_user and current_user.admin:
        if request.method == "POST":
            freelance_job_data: dict = request.get_json()
            # TODO- obtain user id from current_user
            uid: str = current_user.uid
            link_details = "webdev/webdevelopmentmock"
            project_name: str = freelance_job_data['project_name']
            description: str = freelance_job_data['description']
            est_hours_to_complete: int = int(freelance_job_data['est_hours_to_complete'])
            currency: str = freelance_job_data['currency']
            budget: int = int(freelance_job_data['budget'])
            try:
                freelance_job: FreelanceJobModel = FreelanceJobModel(uid=uid, project_name=project_name,
                                                                     project_category="webdev",
                                                                     description=description,
                                                                     budget_allocated=budget,
                                                                     est_hours_to_complete=est_hours_to_complete,
                                                                     currency=currency)

                db.session.add(freelance_job)
                db.session.commit()
            except OperationalError as e:
                return jsonify({"status": "failure", "message": "database error"}), 500
            return jsonify({'message': "freelance job successfully created"}), 202
    else:
        return jsonify({'message': "you are not authorized to perform this action"}), 401


@admin_routes.route('/admin/messages', methods=['GET'])
@token_required
def user_messages(current_user: any) -> any:
    if current_user and current_user.admin:
        try:
            messages: list = [dict(message_) for message_ in ContactModel.query.filter_by(_is_read=False).all()]
        except OperationalError as e:
            return jsonify({"status": "failure", "message": "database error"}), 500

        return jsonify({'message': 'Successfully fetched messages', 'messages': messages}), 200
    else:
        return jsonify({'message': 'You are not authorized to perform this action'}), 401


@admin_routes.route('/admin/messages/all', methods=['GET'])
@token_required
def all_messages(current_user: any) -> any:
    if current_user and current_user.admin:
        try:
            messages = [dict(message_) for message_ in ContactModel.query.filter_by().all()]
        except OperationalError as e:
            return jsonify({"status": "failure", "message": "database error"}), 500
        return jsonify({'message': 'Successfully fetched messages', 'messages': messages}), 200
    else:
        return jsonify({'message': 'You are not authorized to perform this action'}), 401


@admin_routes.route('/admin/message/:<path:path>', methods=['POST', 'GET'])
@token_required
def message(current_user: any, path: str) -> any:
    if current_user and current_user.admin:
        if request.method == "GET":
            try:
                message_ = ContactModel.query.filter_by(_contact_id=path).first()
            except OperationalError as e:
                return jsonify({"status": "failure", "message": "database error"}), 500

            return jsonify({'message': 'Successfully fetched Message', 'response': dict(message_)}), 200
        elif request.method == "POST":
            response_details = request.get_json()
            # TODO - Create ResponseModel
            # TODO - fetch details of response message from response_details and store on ResponseModel
        else:
            return jsonify({'message': 'Invalid Method'}), 401
    else:
        return jsonify({'message': 'You are not authorized to perform this action'}), 401
