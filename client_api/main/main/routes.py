
from flask import render_template, request, make_response, Blueprint, jsonify,flash,get_flashed_messages
from ..library import Metatags, token_required, logged_user
from .models import ContactModel
from .. import db
main = Blueprint('main', __name__)

###########################################################################################################
# Basic Home Page Routes

@main.route('/', methods=['GET', 'POST'])
@logged_user
def home(current_user):
    get_flashed_messages()
    return render_template('index.html', heading="Home",current_user=current_user,
                           menu_open=True, meta_tags=Metatags().set_home())

# noinspection PyArgumentList,PyArgumentList
@main.route('/contact', methods=['GET', 'POST'])
@logged_user
def contact(current_user):
    get_flashed_messages()
    if request.method == "GET":
        return render_template('contact.html', heading="Contact",current_user=current_user,
                               menu_open=True, meta_tags=Metatags().set_contact())

    elif request.method == "POST":
        # TODO- handle post request here
        contact_details = request.get_json()
        print(contact_details)
        return jsonify({"message": "Successfully created new messafe"})

@main.route('/about', methods=['GET'])
@logged_user
def about(current_user):
    get_flashed_messages()
    return render_template('about.html', heading="About", menu_open=True,current_user=current_user, meta_tags=Metatags().set_about())

@main.route('/social/<path:path>', methods=['GET'])
@logged_user
def social(current_user,path):
    get_flashed_messages()
    if path == "twitter":
        return render_template('social/twitter.html', heading="On Twitter",current_user=current_user,
        menu_open=True,meta_tags=Metatags().set_social_twitter())
    elif path == "github":
        return render_template('social/github.html', heading="Github Profile", menu_open=True,meta_tags=Metatags().set_social_github())
    else:
        pass

###########################################################################################################
# Payment Processing Modules

@main.route('/payments', methods=['GET', 'POST'])
@token_required
def payments(current_user):
    get_flashed_messages()
    pass

@main.route('/payment', methods=['GET', 'POST'])
@token_required
def make_payment(current_user):
    get_flashed_messages()
    pass

@main.route('/balances', methods=['GET', 'POST'])
@token_required
def balances(current_ser):
    get_flashed_messages()
    pass

###########################################################################################################
# Basic Website Routes Sitemaps & Robots.txt

@main.route('/terms-of-service')
@logged_user
def terms(current_user):
    get_flashed_messages()
    return render_template('terms.html', heading='Terms of Service',current_user=current_user, menu_open=True, meta_tags=Metatags().set_terms())

@main.route('/privacy-policy')
@logged_user
def privacy(current_user):
    get_flashed_messages()
    return render_template('privacy.html', heading='Privacy Policy', current_user=current_user, menu_open=True, meta_tags=Metatags().set_privacy())

@main.route('/offline')
@logged_user
def offline(current_user):
    get_flashed_messages()
    return render_template('offline.html', heading="Network Connection Lost...",current_user=current_user, menu_open=True, meta_tags=Metatags().set_home())

@main.route('/robots.txt')
def robots():
    response = make_response(render_template('robots.txt'))
    response.headers['content-type'] = 'text/plain'
    return response

@main.route('/sitemap.xml')
def sitemap():
    # TODO- add dynamic sitemap content
    github_repos = []
    codepen_repos = []
    blog_posts = []

    response = make_response(
        render_template('sitemap.xml', github_repos=github_repos, codepen_repos=codepen_repos, blog_posts=blog_posts))
    response.headers['content-type'] = 'text/xml'
    return response

@main.route('/sw.js')
def service_worker():
    response = make_response(render_template('sw.js'))
    response.headers['content-type'] = 'application/javascript'
    return response
# TODO- add a 404 handler here incase no URL was matched