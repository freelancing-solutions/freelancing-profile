from flask_restful import Api, Resource, marshal_with, reqparse, fields


class SlackAPI(Resource):
    """[summary]
        Used to Fetch Slack Chanell Messages for projects
    Args:
        Resource ([type]): [description]
    """