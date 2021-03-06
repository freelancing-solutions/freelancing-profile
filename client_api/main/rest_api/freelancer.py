import time
from flask import jsonify
from flask_restful import Api, Resource, marshal_with, reqparse, fields,abort
from ..hireme.models import FreelanceJobModel
from .. import db
from ..library import is_authenticated, authenticated_user


# uid = db.Column(db.String(128),unique=True, nullable=False)
# project_id = db.Column(db.Integer, primary_key=True)
# project_name = db.Column(db.String(1048), nullable=False)
# project_category = db.Column(db.String(64), nullable=False)
# description = db.Column(db.String(2096), nullable=False)
# progress = db.Column(db.Integer, nullable=False)
# status = db.Column(db.String(32), nullable=False)
# link_details = db.Column(db.String(256), nullable=False)
# time_created = db.Column(db.Integer, nullable=False)
# est_hours_to_complete = db.Column(db.Integer, nullable=False)
# currency = db.Column(db.String(32), nullable=False)
# budget_allocated = db.Column(db.Integer, nullable=False)
# total_paid = db.Column(db.Integer, nullable=False)

class FreelanceJobAPI(Resource):
    """
        Freelancer API, responsible with freelance job creation and management tasks
        Args:
            Resource ([type]): [description]
    """
    freelance_job_fields = {
        "uid" : fields.String,
        "project_id" : fields.Integer,
        "project_name" : fields.String,
        "project_category" : fields.String,
        "description" : fields.String,
        "progress" : fields.Integer,
        "status" : fields.String,
        "link_details" : fields.String,
        "time_created" : fields.Integer,
        "est_hours_to_complete" : fields.Integer,
        "currency" : fields.String,
        "budget_allocated" : fields.String,
        "total_paid" : fields.String
    }


    def __init__(self):
        super(FreelanceJobAPI).__init__()
        self.request_parser = reqparse.RequestParser(bundle_errors=True, trim=True)
        self.request_parser.add_argument('uid', type=str, location='json', required=True, help="User ID is required")
        self.request_parser.add_argument('project_name', type=str, location='json')
        self.request_parser.add_argument('project_category', type=str, location='json')
        self.request_parser.add_argument('description', type=str, location='json')
        self.request_parser.add_argument('currency', type=str, location='json')
        self.request_parser.add_argument('budget_allocated', type=int, location='json')

    @staticmethod
    def create_link_detail(name,cat):

        cat_link = ""
        for cat in cat.split(" "):
            cat_link += cat
        name_link = ""
        for name in name.split(" "):
            name_link += name

        return "/{}/{}".format(cat_link,name_link).encode("UTF-8")


    @marshal_with(freelance_job_fields)
    def get(self,project_id):
        """
            Given a project id return the project indicated
        Args:
            project_id ([type]): [project id auto generated from database]
        Returns:
            [type]: [ Response -> FreelanceJobModel]
        """

        freelance_job = FreelanceJobModel.query.filter_by(project_id=project_id).first()
        if freelance_job is not None:
            return freelance_job
        else:
            abort(http_status_code=404,message='Freelance Job not found')

    @marshal_with(freelance_job_fields)
    def post(self):
        """
            given freelance job arguments from json create new freelance job
            Returns:
                [type]: [freelance_job]
        """

        fj_details = self.request_parser.parse_args()
        # Default is seven days allow user to edit
        hours_to_complete = 24 * 7
        right_now_milliseconds = int(float(time.time()) * 1000)

        project_name = fj_details['project_name']
        project_category = fj_details['project_category']
        if project_name and project_category:
            link_details = self.create_link_detail(name=project_name,cat=project_category)
        else:
            abort(http_status_code=404,message='Invalid Arguments, Project_name or category not specified')
        try:
            freelance_job = FreelanceJobModel(uid=fj_details['uid'],project_name=fj_details['project_name'],
            project_category=fj_details['project_category'],description=fj_details['description'],
            currency=fj_details['currency'], budget_allocated=fj_details['budget_allocated'],
            total_paid=0,status='created',time_created=right_now_milliseconds,
            est_hours_to_complete=hours_to_complete,progress=0,link_details=link_details)

            db.session.add(freelance_job)
            db.session.commit()
        except Exception as error:
            abort(http_status_code=500, message="Something snapped its not your fault try again later")

        return freelance_job

    @marshal_with(freelance_job_fields)
    def put(self,project_id):
        """
            Given freelance job arguments update freelance job
        Args:
            project_id ([type]): [The id of the project or feelance job to update]

        Returns:
            [type]: [Returns the updated freelance job]
        """
        fj_details = self.request_parser.parse_args()
        freelance_job = FreelanceJobModel.query.filter_by(project_id=project_id)

        if freelance_job is not None:
            freelance_job.update(dict(fj_details))
            db.session.commit()
            return freelance_job.first()
        else:
            abort(http_status_code=404,message='Freelance job not found')


class ListFreelanceJobs(Resource):
    """
        ListFreelanceJobs displays a list of freelance jobs
    Args:
        Resource ([type]): [description]
    """

    def __init__(self):
        super(ListFreelanceJobs).__init__()
        self.args_parser = reqparse.RequestParser(bundle_errors=True, trim=True)
        self.args_parser.add_argument('x-access-token', type=str, location="headers")


    def get(self):

        arguments = self.args_parser.parse_args()
        access_token = arguments['x-access-token']
        current_user = authenticated_user(token=access_token)
        if current_user is None:
            abort(http_status_code=401,message="User not Authenticated")

        payload = [dict(freelance_job) for freelance_job in FreelanceJobModel.query.filter_by(uid=current_user.uid).all()]
        return jsonify({"status": True, "payload": payload, "error": ""})

