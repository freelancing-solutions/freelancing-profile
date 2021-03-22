from .. import db
from flask import current_app


class ProjectRepos(db.Model):
    """
        Model to store details about My projects and profiles

    Args:
        db ([type]): [description]
    """
    __bind_key__ = "app"