# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
from flask import Flask, escape, abort, make_response, jsonify, render_template, request, url_for
# from flask_restful import Api, Resource, marshal_with, reqparse, fields
# from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, static_folder="static", template_folder="templates")
# api = Api(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html', heading="Home")


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html', heading="Contact")


@app.route('/blog', methods=['GET', 'POST'])
def blog():
    return render_template('blog.html', heading="Blog")


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html', heading="About")


@app.route('/projects', methods=['GET', 'POST'])
def projects():
    return render_template('projects.html', heading="Projects")


@app.route('/hire-freelancer', methods=['GET', 'POST'])
def freelancer():
    return render_template('freelancer.html', heading="Freelancer")


@app.route('/robots.txt')
def robots():
    return render_template('robots.txt')


@app.route('/sitemap.xml')
def sitemap():
    # TODO- add dynamic sitemap content
    return render_template('sitemap.xml')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
