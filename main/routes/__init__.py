
from main import app
from flask import render_template, make_response, request
from main.applibs import Metatags

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html',
                            heading="Home",
                            menu_open=True,
                            meta_tags=Metatags().set_home()
                            )


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == "GET":
        return render_template('contact.html',
            heading="Contact",
            menu_open=True,
            meta_tags=Metatags().set_contact()
            )
    else:
        # TODO- handle post request here
        pass


@app.route('/blog', methods=['GET', 'POST'])
def blog():
    if request.method == "GET":
        return render_template('blog.html', heading="Blog", menu_open=True, meta_tags=Metatags().set_blog())
    else:
        pass

@app.route('/blog/categories/<path:path>', methods=['GET', 'POST'])
def blog_categories(path):
    if path == "front-end":
        # TODO- Fetch Front end Posts
        return render_template('blog/frontend.html', heading="Front End Development Articles", menu_open=True, meta_tags=Metatags().set_blog())
    elif path == "back-end":
        return render_template('blog/backend.html', heading="Back End Development Articles", menu_open=True, meta_tags=Metatags().set_blog())
    elif path == "api":
        return render_template('blog/api.html', heading="API Development Articles", menu_open=True, meta_tags=Metatags().set_blog())
    else:
        # TODO- add categories list as default
        pass

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html', heading="About", menu_open=True, meta_tags=Metatags().set_about())


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

@app.route('/projects/repos/<path:path>', methods=['GET'])
def projects_repos(path):
    if path == "github":
        return render_template('projects/github.html', heading="Github Repositories", meta_tags=Metatags().set_projects())
    elif path == "codepen":
        return render_template('projects/codepen.html', heading="Codepen Repositories", meta_tags=Metatags().set_projects())
    else:
        return render_template('projects/repos.html', heading="Project Repositories", meta_tags=Metatags().set_projects())


@app.route('/hire-freelancer', methods=['GET', 'POST'])
def freelancer():
    if request.method == "GET":
        return render_template('hireme.html', heading="Hiring a Freelancer", meta_tags=Metatags().set_freelancer())
    else:
        pass

@app.route('/hire-freelancer/<path:path>', methods=['GET', 'POST'])
def hire(path):
    if path == 'login':
        return render_template('hireme/login.html', heading="Login", meta_tags=Metatags().set_freelancer())
    elif path == "gigs":
        return render_template('hireme/gigs.html', heading="My Previous Gigs", meta_tags=Metatags().set_freelancer())
    elif path == "hire":
        return render_template('hireme/hire.html', heading="Hire a Freelancer", meta_tags=Metatags().set_freelancer())
    else:
        return render_template('404.html', heading="Not Found", meta_tags=Metatags().set_home())

    #  Basic Pages

@app.route('/terms-of-service')
def terms():
    return render_template('terms.html', heading='Terms of Service', menu_open=True, meta_tags=Metatags().set_home())

@app.route('/privacy-policy')
def privacy():
    return render_template('privacy.html', heading='Privacy Policy', menu_open=True, meta_tags=Metatags().set_home())


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
    github_repos = []
    codepen_repos = []
    blog_posts = []

    response = make_response(render_template('sitemap.xml', github_repos=github_repos, codepen_repos=codepen_repos, blog_posts=blog_posts ))
    response.headers['content-type'] = 'text/xml'
    return response


@app.route('/sw.js')
def service_worker():
    response = make_response(render_template('sw.js'))
    response.headers['content-type'] = 'application/javascript'
    return response

# TODO- add a 404 handler here incase no URL was matched
