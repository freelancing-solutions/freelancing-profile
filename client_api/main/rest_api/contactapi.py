from flask import jsonify
from flask_restful import Api, Resource, marshal_with, reqparse, fields, abort
import requests
from ..main.models import ContactModel
from .. import db
from ..library import token_required, authenticated_user



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
        self.contact_req_parse.add_argument('x-access-token', type=str, location='headers')

    def parse_contact_args(self):
        print("parsing")
        self.contact_req_parse.add_argument('names', type=str, location='json')
        self.contact_req_parse.add_argument('email', type=str, location='json')
        self.contact_req_parse.add_argument('cell', type=str, location='json')
        self.contact_req_parse.add_argument('reason', type=str, location='json')
        self.contact_req_parse.add_argument('subject', type=str, location='json')
        self.contact_req_parse.add_argument('body', type=str, location='json')
        return self.contact_req_parse.parse_args()


    def post(self):
        """
            create new contact from details and save to backend
        """

        contact_form = self.parse_contact_args()
        print(contact_form)
        current_user = authenticated_user(token=contact_form['x-access-token'])
        print(current_user)
        contact = ContactModel(uid=current_user.uid,
                              names=contact_form['names'],
                              email=contact_form['email'],
                              cell=contact_form['cell'],
                              subject=contact_form['subject'],
                              body=contact_form['body'],
                              reason=contact_form['reason'])
        db.session.add(contact)
        db.session.commit()

        response = {
            'uid': contact.uid,
            'contact_id': contact.contact_id,
            'names': contact.names,
            'email': contact.email,
            'cell': contact.cell,
            'reason': contact.reason,
            'subject': contact.subject,
            'body': contact.body
        }
        return jsonify({'status': True, "payload": response, "error": ""})

    @token_required
    def get(self,current_user, contact_id):
        """
            Can be invked by a logged in user or by admin to obtain a list of contact messages
        Args:
            current_user ([type]): [description]
            contact_id ([type]): [description]

        Returns:
            [type]: [description]
        """
        if current_user.admin is True:
            results = []
            contact_list = ContactModel.query.filter_by().all()
            for contact in contact_list:
                results.append(dict(contact))
                return jsonify({"status": True, "payload": results, "error": ""}), 200
        else:
            contact = ContactModel.query.filter_by(contact_id=contact_id).first()
            if contact is not None:
                return jsonify({ "status":True, "payload":dict(contact),"error": ""}), 200
            else:
                abort(http_status_code=404, message='Contact not found')


    @marshal_with(contact_fields)
    @token_required
    def put(self,current_user, contact_id):
        """
            update contact details depending on contact id
        :param contact_id:
        :return:
        """
        # If you are not admin then you must own the Contact record in order to update it
        if current_user.admin is True:
            contact_model = ContactModel.query.filter_by(contact_id=contact_id)
        else:
            contact_model = ContactModel.query.filter_by(contact_id=contact_id, uid=current_user.uid)

        if contact_model is not None:
            contact_form = self.parse_contact_args()
            contact_model.update(dict(contact_form))

            db.session.commit()
            return contact_model.first()
        else:
            abort(http_status_code=404, message='Contact not found')

