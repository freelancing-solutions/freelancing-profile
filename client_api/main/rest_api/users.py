from flask import make_response
from flask_login import login_user
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from ..users.models import UserModel
from .. import db
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

user_fields = {
        'id':fields.Integer,
        'uid': fields.String,
        'username': fields.String,
        'email': fields.String,
        'username': fields.String,
        'cell': fields.String,
        'names': fields.String,
        'surname': fields.String,
        'admin': fields.Boolean
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

    @marshal_with(user_fields)
    def get(self,uid):
        """
            Accessed by admin Get User
        """
        user_detail = UserModel.query.filter_by(uid=uid).first()
        if user_detail is not None:
            return user_detail
        abort(http_status_code=404,message="user not found")

    @marshal_with(user_fields)
    def post(self):
        """
            Create new User by admin
        """
        self.args_parser.add_argument('cell', type=str, location='json')
        self.args_parser.add_argument('names', type=str, location='json')
        self.args_parser.add_argument('surname', type=str, location='json')
        self.args_parser.add_argument('username', type=str, location='json')
        self.args_parser.add_argument('admin', type=bool, location='json')
        self.args_parser.add_argument('password', type=str, location='json')
        self.args = self.args_parser.parse_args()
        email = self.args['email']
        username = self.args['username']
        uid = str(uuid.uuid4())
        cell = self.args['cell']
        names = self.args['names']
        surname = self.args['surname']
        admin = self.args['admin']

        password_hash = generate_password_hash(self.args['password'],method='sha256')
        user_detail = UserModel(uid=uid,email=email,username=username,cell=cell,names=names,surname=surname,admin=admin,password=password_hash)
        db.session.add(user_detail)
        db.session.commit()
        return user_detail

    @marshal_with(user_fields)
    def put(self):
        """
            Update User Details by admin
        """
        self.args_parser.add_argument('cell', type=str, location='json')
        self.args_parser.add_argument('names', type=str, location='json')
        self.args_parser.add_argument('username', type=str, location='json')
        self.args_parser.add_argument('surname', type=str, location='json')
        self.args_parser.add_argument('admin', type=bool, location='json')
        self.args_parser.add_argument('password', type=str, location='json')
        self.args = self.args_parser.parse_args()

        email = self.args['email']
        username = self.args['username']
        cell = self.args['cell']
        names = self.args['names']
        surname = self.args['surname']
        admin = self.args['admin']
        password_hash = generate_password_hash(self.args['password'],method='sha256')
        user_detail = UserModel.query.filter_by(email=email)
        if user_detail is not None:
            # TODO - email might need to be verified again if changed
            user_detail.email = email
            user_detail.username = username
            # TODO- cell might need to be verified if changed
            user_detail.cell = cell
            user_detail.names = names
            user_detail.surname = surname
            user_detail.admin = admin
            user_detail.password = password_hash
            db.session.merge(user_detail)
            db.session.flush()
            db.session.commit()
            return user_detail.first()
        else:
            abort(http_status_code=404,message="user not found")

    @marshal_with(user_fields)
    def delete(self,uid):
        """
            Delete User by Admin
        """
        user_detail = UserModel.query.filter_by(uid=uid).first()
        if user_detail is not None:
            db.session.delete(user_detail)
            db.session.commit()