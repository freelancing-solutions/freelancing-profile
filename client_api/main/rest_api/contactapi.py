from flask_restful import Api, Resource, marshal_with, reqparse, fields, abort


class ContactAPI(Resource):
    """
        Contact Form Rest API
        The rest API will deal with form data, that is fetching contact
        details, storing contact details, and also updating and deleting feedbacks
    """
    __contact_store_route = ''

    def __init__(self):
        self.contact_req_parse = reqparse.RequestParser(bundle_errors=True)
        self.contact_req_parse.add_argument('Authentication', type=str, location='headers')
        super(ContactAPI, self).__init__()

    def parse_contact_args(self):
        self.contact_req_parse.add_argument('names', type=str, location='json', required=True, help="Names should be specified")
        self.contact_req_parse.add_argument('email', type=str, location='json', required=True, help='Email Address is required' )
        self.contact_req_parse.add_argument('cell', type=str, location='json', required=True, help='Cell Number is required')
        self.contact_req_parse.add_argument('reason', type=str, location='json', required=True, help='Contact Reason is required')
        self.contact_req_parse.add_argument('freelance_job_id', type=str, location='json')
        self.contact_req_parse.add_argument('support_type', type=str, location='json')
        self.contact_req_parse.add_argument('subject', type=str, location='json', required=True, help='Subject is required')
        self.contact_req_parse.add_argument('body', type=str, location='json', required=True, help='Message body is required')
        self.contact_req_parse.parse_args()
        return self.contact_req_parse

    def post(self):
        contact_form_json = self.parse_contact_args()
        #TODO- Send Data to Backend Store by calling function- through Pub-Sub





    def get(self):
        pass

    def put(self):
        pass