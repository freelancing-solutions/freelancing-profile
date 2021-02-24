
from flask import render_template, request, make_response, Blueprint
from client_api.main import Metatags

main = Blueprint('main', __name__)


###########################################################################################################
# Basic Home Page Routes

@main.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html', heading="Home",
                           menu_open=True, meta_tags=Metatags().set_home())


# noinspection PyArgumentList,PyArgumentList
@main.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == "GET":
        return render_template('contact.html', heading="Contact",
                               menu_open=True, meta_tags=Metatags().set_contact())
    elif request.method == "POST":
        # TODO- handle post request here
        print(request.args)
        return render_template('contact.html', heading="Contact",
                               menu_open=True, meta_tags=Metatags().set_contact())


@main.route('/about', methods=['GET'])
def about():
    return render_template('about.html', heading="About", menu_open=True, meta_tags=Metatags().set_about())


###########################################################################################################
# Basic Website Routes Sitemaps & Robots.txt

@main.route('/terms-of-service')
def terms():
    return render_template('terms.html', heading='Terms of Service', menu_open=True, meta_tags=Metatags().set_home())


@main.route('/privacy-policy')
def privacy():
    return render_template('privacy.html', heading='Privacy Policy', menu_open=True, meta_tags=Metatags().set_home())


@main.route('/offline')
def offline():
    return render_template('offline.html', heading="Network Connection Lost...", meta_tags=Metatags().set_home())


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
