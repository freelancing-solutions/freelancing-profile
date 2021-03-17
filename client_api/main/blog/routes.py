from flask import render_template, request, Blueprint, flash, get_flashed_messages
from ..library import Metatags, logged_user
blog_bp = Blueprint('blog', __name__, static_folder="static", template_folder="templates")


###########################################################################################################
# Blog Routes
@blog_bp.route('/blog', methods=['GET'])
@logged_user
def blog(current_user):
    get_flashed_messages()
    if request.method == "GET":
        return render_template('blog.html', heading="Blog", menu_open=True,
                               current_user=current_user, meta_tags=Metatags().set_blog())
    else:
        return render_template('404.html', heading="Page Not Found", menu_open=True,
                               current_user=current_user, meta_tags=Metatags().set_blog())


@blog_bp.route('/blog/articles/<path:path>')
@logged_user
def frontend_articles(current_user,path):
    get_flashed_messages()
    if request.method == "GET":
        if path == "service-workers/custom-service-worker-with-push-notifications":
            title = "Custom Service Worker with push Notifications"
            template = 'blog/frontend_articles/service_workers.html'
            return render_template(template, current_user=current_user, heading=title, meta_tags=Metatags().set_blog())

        elif path == "python/testing/using-pytest-for-alchemy-models":
            title = "Using Pytest to test Alchemy Models"
            template = 'blog/backend_articles/pytest-alchemy-models.html'
            return render_template(template, current_user=current_user, heading=title, meta_tags=Metatags().set_blog())


@blog_bp.route('/blog/categories/<path:path>', methods=['GET'])
@logged_user
def blog_categories(current_user, path):
    get_flashed_messages()
    if path == "front-end":
        title = "Front End Development Articles"
        template = 'blog/frontend.html'
        return render_template(template, heading=title, menu_open=True, current_user=current_user,
                               meta_tags=Metatags().set_blog())
    elif path == "back-end":
        title = 'Back End Development Articles'
        template = 'blog/backend.html'
        return render_template(template, heading=title, menu_open=True, current_user=current_user,
                               meta_tags=Metatags().set_blog())
    elif path == "api":
        title = 'API Development Articles'
        template = 'blog/api.html'
        return render_template(template, heading=title, menu_open=True, current_user=current_user,
                               meta_tags=Metatags().set_blog())
    else:
        return render_template('404.html', heading="Page Not Found", menu_open=True,
                               current_user=current_user, meta_tags=Metatags().set_blog())


@blog_bp.route('/learn-more/<path:path>', methods=['GET'])
@logged_user
def learn_more(current_user,path):
    get_flashed_messages()
    if path == "backend-development":
        title = 'Learn More Back End Development'
        template = 'learnmore/backend.html'
        return render_template(template, heading=title, current_user=current_user, menu_open=True,
                               meta_tags=Metatags().set_learn_backend())
    elif path == "frontend-development":
        title = 'Learn More Front End Development'
        template = 'learnmore/frontend.html'
        return render_template(template, heading=title, current_user=current_user, menu_open=True,
                               meta_tags=Metatags().set_learn_frontend())
    else:
        return render_template("404.html", heading="Page Not Found", 
        current_user=current_user,meta_tags=Metatags().set_home())
