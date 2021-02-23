import os
from flask import Flask, make_response, escape, abort, make_response, jsonify, render_template, request, url_for
# from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from applibs import Metatags
from rest_api import Contact, Blog, Freelancer, Github, Sitemap

app = Flask(__name__, static_folder="static", template_folder="templates")
api = Api(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html', heading="Home", meta_tags=Metatags().set_home())


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == "GET":
        return render_template('contact.html', heading="Contact", meta_tags=Metatags().set_contact())
    else:
        # TODO- handle post request here
        pass


@app.route('/blog', methods=['GET', 'POST'])
def blog():
    if request.method == "GET":
        return render_template('blog.html', heading="Blog", meta_tags=Metatags().set_blog())
    else:
        pass


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html', heading="About", meta_tags=Metatags().set_about())


@app.route('/learn-more/<path:path>', methods=['GET'])
def learn_more(path):
    if path == "backend-development":
        return render_template('learnmore/backend.html',
                            heading="Learn More Back End Development",
                            meta_tags=Metatags().set_learn_backend())
    elif path == "frontend-development":
        return render_template('learnmore/frontend.html',
                                heading="Learn More Front End Development",
                                meta_tags=Metatags().set_learn_frontend())
    else:
        return render_template("404.html", heading="Not Found", meta_tags=Metatags().set_home())

@app.route('/projects', methods=['GET', 'POST'])
def projects():
    if request.method == "GET":
        return render_template('projects.html', heading="Projects", meta_tags=Metatags().set_projects())
    else:
        pass

@app.route('/hire-freelancer', methods=['GET', 'POST'])
def freelancer():
    if request.method == "GET":
        return render_template('hireme.html', heading="Hire a Freelancer", meta_tags=Metatags().set_freelancer())
    else:
        pass

@app.route('/offline')
def offline():
    return render_template('offline.html', heading="Network Connection Lost...", meta_tags=Metatags().set_home())


@app.route('/robots.txt')
def robots():
    response = make_response(render_template('robots.txt'))
    response.headers['content-type'] = 'text/plain'
    return response


@app.route('/sitemap.xml')
def sitemap():
    # TODO- add dynamic sitemap content
    response = make_response(render_template('sitemap.xml'))
    response.headers['content-type'] = 'text/xml'
    return response


@app.route('/sw.js')
def service_worker():
    response = make_response(render_template('sw.js'))
    response.headers['content-type'] = 'application/javascript'
    return response


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
