from flask_restful import Api, Resource, marshal_with, reqparse, fields, abort
import requests

contact_api_fields = {
    'status': fields.Boolean,
    'payload': {
        'uid': fields.String,
        'contact_id': fields.String,
        'names': fields.String,
        'email': fields.String,
        'cell': fields.String,
        'reason': fields.String,
        'freelance_job_id': fields.String,
        'support_type': fields.String,
        'subject': fields.String,
        'body': fields.String
    },
    'error': fields.String
}

contact_list_fields = {
    'status': fields.Boolean,
    'payload': fields.List,
    'error': fields.String
}


class ContactAPI(Resource):
    """
        Contact Form Rest API
        The rest API will deal with form data, that is fetching contact
        details, storing contact details, and also updating and deleting feedbacks
    """
    __contact_store_route = ''

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
        self.contact_req_parse.add_argument('freelance_job_id', type=str, location='json')
        self.contact_req_parse.add_argument('support_type', type=str, location='json')
        self.contact_req_parse.add_argument('subject', type=str, location='json', required=True,
                                            help='Subject is required')
        self.contact_req_parse.add_argument('body', type=str, location='json', required=True,
                                            help='Message body is required')
        return self.contact_req_parse.parse_args(strict=True)

    @marshal_with(contact_api_fields)
    def post(self):
        """
            create new contact form details and save to backend
        """
        contact_form_json = self.parse_contact_args()
        # TODO- Send Data to Backend Store by calling function- through Pub-Sub
        pass

    @marshal_with(contact_list_fields)
    def get(self, uid):
        """
            return contact fields dependent on the user
        :param uid:
        :return:
        """
        pass

    @marshal_with(contact_api_fields)
    def put(self, contact_id):
        """
            update contact details depending on contact id
        :param contact_id:
        :return:
        """
        pass
