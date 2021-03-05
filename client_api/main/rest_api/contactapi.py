from flask_restful import Api, Resource, marshal_with, reqparse, fields, abort
import requests
from main.main.models import ContactModel
from main import db



class ContactAPI(Resource):
    """
        Contact Form Rest API
        The rest API will deal with form data, that is fetching contact
        details, storing contact details, and also updating and deleting feedbacks
    """
    __contact_store_route = ''
    contact_fields = {
            'uid': fields.String,
            'contact_id': fields.String,
            'names': fields.String,
            'email': fields.String,
            'cell': fields.String,
            'reason': fields.String,
            'subject': fields.String,
            'body': fields.String
    }

    def __init__(self):
        super(ContactAPI, self).__init__()
        self.contact_req_parse = reqparse.RequestParser(bundle_errors=True,trim=True)
        self.contact_req_parse.add_argument('Authentication', type=str, location='headers')

    def parse_contact_args(self):
        self.contact_req_parse.add_argument('contact_id', type=str, location='json')
        self.contact_req_parse.add_argument('uid', type=str, location='json')
        self.contact_req_parse.add_argument('names', type=str, location='json', required=True,
                                            help='Names should be specified')
        self.contact_req_parse.add_argument('email', type=str, location='json', required=True,
                                            help='Email Address is required')
        self.contact_req_parse.add_argument('cell', type=str, location='json', required=True,
                                            help='Cell Number is required')
        self.contact_req_parse.add_argument('reason', type=str, location='json', required=True,
                                            help='Contact Reason is required')
        self.contact_req_parse.add_argument('subject', type=str, location='json', required=True,
                                            help='Subject is required')
        self.contact_req_parse.add_argument('body', type=str, location='json', required=True,
                                            help='Message body is required')
        return self.contact_req_parse.parse_args(strict=True)

    @marshal_with(contact_fields)
    def post(self):
        """
            create new contact from details and save to backend
        """
        contact_form = self.parse_contact_args()
        contact = ContactModel(uid=contact_form['uid'],
                              names=contact_form['names'],
                              email=contact_form['email'],
                              cell=contact_form['cell'],
                              subject=contact_form['subject'],
                              body=contact_form['body'],
                              reason=contact_form['reason'])
        db.session.add(contact)
        db.session.commit()

        return contact

    @marshal_with(contact_fields)
    def get(self, contact_id):
        contact = ContactModel.query.filter_by(contact_id=contact_id).first()
        if contact is not None:
            return contact
        else:
            abort(http_status_code=404, message='Contact not found')


    @marshal_with(contact_fields)
    def put(self, contact_id):
        """
            update contact details depending on contact id
        :param contact_id:
        :return:
        """

        contact_model = ContactModel.query.filter_by(contact_id=contact_id)
        if contact_model is not None:
            contact_form = self.parse_contact_args()
            contact_model.update(dict(contact_form))

            db.session.commit()
            return contact_model.first()
        else:
            abort(http_status_code=404, message='Contact not found')
