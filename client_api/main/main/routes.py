from flask import render_template, request, make_response, Blueprint, jsonify, flash, get_flashed_messages, current_app
from sqlalchemy.exc import OperationalError

from ..app_settings_store.settingsModels import SiteMapsModel
from ..library import Metatags, token_required, logged_user
from .models import ContactModel
from .. import server_stats_logger
from .. import cache
from ..library.utils import const

main = Blueprint('main', __name__, static_folder="../static", template_folder="../templates")

###########################################################################################################
# Basic Home Page Routes

# TODO- consider adding a caching layer to cache requests here- the best option is to create a caching wrapper
# working in tandem with logged user or token_required

default_urls_list: list = [
    '/', '/about', '/contact', '/tech-articles',
    '/projects', '/privacy-policy', '/terms-of-service',
    '/learn-more/frontend-development',
    '/learn-more/backend-development',
    '/hire-freelancer',
    '/freelance-articles/how-to/create-freelancing-account',
    '/freelance-articles/how-to/submit-freelance-jobs',
    '/freelance-articles/how-to/download-install-slack',
    '/freelance-articles/how-to/download-install-teamviewer',
    '/freelance-articles/how-to/create-a-github-account',
    '/freelance-articles/how-to/create-a-gcp-developer-account',
    '/freelance-articles/how-to/create-a-heroku-developer-account',
    '/freelance-articles/expectations/communication-channels-procedures',
    '/freelance-articles/expectations/payments-procedures-methods',
    '/freelance-articles/expectations/due-diligence',
    '/freelance-articles/expectations/handing-over-procedures',
    '/freelance-articles/expectations/maintenance-procedures'
]

resource_files_list: list = [
    '/static/plugins/jquery/jquery.min.js',
    '/static/plugins/bootstrap/js/bootstrap.bundle.min.js',
    '/static/js/handlebars.js',
    '/static/js/adminlte.min.js',
    '/static/css/adminlte.min.css',
    '/static/css/ionicons.min.css',
    '/static/plugins/fontawesome-free/css/all.min.css'
]


# cache timeout in seconds
@main.route('/', methods=['GET', 'POST'])
@cache.cached(timeout=const.cache_timeout_hour)
@logged_user
def home(current_user: any) -> tuple:
    get_flashed_messages()

    return render_template('index.html', heading="Home", current_user=current_user,
                           menu_open=True, meta_tags=Metatags().set_home()), 200


@main.route('/contact', methods=['GET', 'POST'])
@logged_user
def contact(current_user: any) -> tuple:
    get_flashed_messages()
    if request.method == "GET":
        return render_template('contact.html', heading="Contact", current_user=current_user,
                               menu_open=True, meta_tags=Metatags().set_contact()), 200

    elif request.method == "POST":
        # TODO- handle post request here
        contact_details = request.get_json()

        if current_user:
            uid = current_user.uid
        else:
            uid = None
        names = contact_details['names']
        if not names:
            return jsonify({"status": "failure", "message": "names cannot be Null"}), 500

        email = contact_details['email']
        if not email:
            return jsonify({"status": "failure", "message": "email cannot be Null"}), 500

        cell = contact_details['cell']
        if not cell:
            return jsonify({"status": "failure", "message": "cell cannot be Null"}), 500

        subject = contact_details['subject']
        if not subject:
            return jsonify({"status": "failure", "message": "subject cannot be Null"}), 500

        body = contact_details['body']
        if not body:
            return jsonify({"status": "failure", "message": "body cannot be Null"}), 500

        reason = contact_details['reason']
        if not reason:
            return jsonify({"status": "failure", "message": "reason cannot be Null"}), 500

        try:
            contact_instance = ContactModel(names=names, email=email, cell=cell, subject=subject, body=body,
                                            reason=reason, uid=uid)
        except OperationalError as error:
            return jsonify({'status': "failure", "message": "error connecting or operating on database"}), 500

        if contact_instance:
            return jsonify({"message": "Message Successfully sent, I will get back to you"}), 200
        else:
            return jsonify({'message': "Error Sending message"}), 500
    else:
        pass


@main.route('/about', methods=['GET'])
@cache.cached(timeout=const.cache_timeout_hour)
@logged_user
def about(current_user: any) -> tuple:
    get_flashed_messages()
    return render_template('about.html', heading="About", menu_open=True,
                           current_user=current_user, meta_tags=Metatags().set_about()), 200


@main.route('/social/<path:path>', methods=['GET'])
@cache.cached(timeout=const.cache_timeout_hour)
@logged_user
def social(current_user: any, path: str) -> tuple:
    get_flashed_messages()
    if path == "twitter":
        return render_template('social/twitter.html', heading="On Twitter", current_user=current_user,
                               menu_open=True, meta_tags=Metatags().set_social_twitter()), 200
    elif path == "github":
        return render_template('social/github.html', heading="Github Profile", menu_open=True,
                               meta_tags=Metatags().set_social_github()), 200
    else:
        return render_template('404.html', heading="Not Found", menu_open=True,
                               current_user=current_user, meta_tags=Metatags().set_home()), 404


###########################################################################################################
# Basic Website Routes Sitemaps & Robots.txt


@main.route('/terms-of-service')
@cache.cached(timeout=const.cache_timeout_hour)
@logged_user
def terms(current_user: any) -> tuple:
    get_flashed_messages()
    return render_template('terms.html', heading='Terms of Service', current_user=current_user,
                           menu_open=True, meta_tags=Metatags().set_terms()), 200


@main.route('/privacy-policy')
@cache.cached(timeout=const.cache_timeout_hour)
@logged_user
def privacy(current_user: any) -> tuple:
    get_flashed_messages()
    return render_template('privacy.html', heading='Privacy Policy', current_user=current_user,
                           menu_open=True, meta_tags=Metatags().set_privacy()), 200


@main.route('/offline')
@cache.cached(timeout=const.cache_timeout_hour)
@logged_user
def offline(current_user: any) -> tuple:
    get_flashed_messages()
    return render_template('offline.html', heading="Network Connection Lost...",
                           current_user=current_user, menu_open=True, meta_tags=Metatags().set_home()), 200


@main.route('/robots.txt')
@cache.cached(timeout=const.cache_timeout_hour)
def robots() -> str:
    response = make_response(render_template('robots.txt'))
    response.headers['content-type'] = 'text/plain'
    return response


@main.route('/sitemap.xml')
@cache.cached(timeout=const.cache_timeout_hour)
def sitemap() -> str:
    # TODO- when adding dynamic content also add sitemap links- when removing do the same
    blog_sitemap_resource = current_app.config['BLOGGING_SITEMAP']
    github_sitemap_resource_name = current_app.config['GITHUB_SITEMAP']
    codepen_resource_name = current_app.config['CODEPEN_SITEMAP']
    dynamic_blog_posts_links = SiteMapsModel.query.filter_by(resource_name=blog_sitemap_resource).all()
    github_sitemap_links = SiteMapsModel.query.filter_by(resource_name=github_sitemap_resource_name).all()
    codepen_sitemap_links = SiteMapsModel.query.filter_by(resource_name=codepen_resource_name).all()

    response = make_response(
        render_template('sitemap.xml', github_repos=[sitemap.link for sitemap in github_sitemap_links],
                        codepen_repos=[sitemap.link for sitemap in codepen_sitemap_links],
                        blog_posts=[sitemap.link for sitemap in dynamic_blog_posts_links]))
    response.headers['content-type'] = 'text/xml'
    return response


@main.route('/sw.js')
def service_worker() -> str:
    # TODO gather a list of urls to store in browser cache
    cache_list: list = default_urls_list + resource_files_list + SiteMapsModel.return_all_dynamic_links()
    response = make_response(render_template('sw.js', cache_list=cache_list))
    response.headers['content-type'] = 'application/javascript'
    return response


# Statistics
# TOD
@main.route('/logger')
def logger() -> tuple:
    return render_template('stats/logger.html',
                           heading="Server Stats",
                           stats_logger=server_stats_logger,
                           meta_tags=Metatags().set_home(),
                           menu_open=True), 200


@main.route('/logger-json', methods=['GET'])
def logger_json() -> tuple:
    return jsonify({'status': 'success', 'payload': server_stats_logger.__dict__()}), 200


@main.route('/unique-visitor', methods=['GET'])
def unique_visitor() -> tuple:
    server_stats_logger.add_unique_visitor()
    print("counting visitors")
    return jsonify({"status": "success", "payload": {
        "visitor": server_stats_logger.unique_visitor,
        "return-visitor": server_stats_logger.return_visitor
    }}), 200


@main.route('/return-visitor', methods=['GET'])
def return_visitor() -> tuple:
    server_stats_logger.add_return_visitor()
    print("counting visitors")
    return jsonify({"status": "success", "payload": {
        "visitor": server_stats_logger.unique_visitor,
        "return-visitor": server_stats_logger.return_visitor
    }}), 200


@main.route('/site-secret', methods=["POST"])
@cache.cached(timeout=const.cache_timeout_hour)
def site_secret() -> tuple:
    print("fetching site secret")
    secret = current_app.config.get('SECRET')
    print(secret)
    return jsonify({"status": "success", "secret": current_app.config.get('SECRET')}), 200


@main.route('/page-view', methods=['GET'])
def page_view() -> tuple:
    return jsonify({"status": "success", "page_views": server_stats_logger.add_page_view()}), 200

