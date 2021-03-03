from flask import make_response
from flask_login import login_user
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from main.users.models import UserModel
from main import db

user_api_marshal_dict = {
    'status': fields.Boolean,
    'payload': {
        'id':fields.Integer,
        'uid': fields.String,
        'username': fields.String,
        'email': fields.String,
        'cell': fields.String,
        'names': fields.String,
        'surname': fields.String
    },
    'error': fields.String
}

class UserAPI(Resource):
    """
        Args:
            Resource ([type]): [description]
    """

    def __init__(self):
        super(UserAPI, self).__init__()
        self.args_parser = reqparse.RequestParser(bundle_errors=True,trim=True)
        self.args_parser.add_argument('email', type=str, location='json', required=True, help='Email is a required field')
        self.args_parser.add_argument('uid', type=str, location='json', required=True, help='User ID cannot be empty')

    @marshal_with(user_api_marshal_dict)
    def get(self,uid):
        """
            Find User and Login User
        """
        self.args = self.args_parser.parse_args()
        email = self.args['email']
        uid = self.args['uid']

        user_detail = UserModel.query.filter_by(uid=uid).first()
        print(user_detail)

    @marshal_with(user_api_marshal_dict)
    def post(self):
        """
            Create new User
        """
        print("Executing post")
        self.args = self.args_parser.parse_args()
        email = self.args['email']
        uid = self.args['uid']

        user_detail = UserModel.query.filter_by(email=email).first()
        print(user_detail)
        if user_detail is None:
            user = UserModel()
            if user.add_user(email=email,uid=uid):
                return {'status': True, 'payload':user_detail,'error':''}
            else:
                return {'status': True, 'payload':{},'error':'Unable to create new user'}
        else:
            return {'status': False, 'payload':{}, 'error': 'User not found'}

    def put(self):
        """
            Updates User details
        """
        self.args_parser.add_argument('')

    def delete(self):
        """
            Delete User
        """
        pass