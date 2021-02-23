import os
from flask import Flask, make_response, escape, abort, make_response, jsonify, render_template, request, url_for
# from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from main.rest_api import Contact, Blog, Freelancer, Github, Sitemap

app = Flask(__name__, static_folder="static", template_folder="templates")
api = Api(app)

from main import routes
