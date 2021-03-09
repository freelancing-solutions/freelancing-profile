from flask import render_template, request, Blueprint,flash,get_flashed_messages
from ..library import Metatags,logged_user
blog_bp = Blueprint('blog', __name__)

###########################################################################################################
# Blog Routes
@blog_bp.route('/blog', methods=['GET'])
@logged_user
def blog(current_user):
    get_flashed_messages()
    if request.method == "GET":
        return render_template('blog.html',heading="Blog",menu_open=True,
        current_user=current_user,meta_tags=Metatags().set_blog())
    else:
        return render_template('404.html',heading="Page Not Found",menu_open=True,
        current_user=current_user,meta_tags=Metatags().set_blog())

@blog_bp.route('/blog/articles/service-workers/custom-service-worker-with-push-notifications')
@logged_user
def frontend_articles(current_user):
    get_flashed_messages()
    if request.method == "GET":
        return render_template('blog/frontend_articles/service_workers.html', heading="Custom Service Worker with push Notifications",
        meta_tags=Metatags().set_blog())



@blog_bp.route('/blog/categories/<path:path>', methods=['GET'])
@logged_user
def blog_categories(current_user,path):
    get_flashed_messages()
    if path == "front-end":
        return render_template('blog/frontend.html',heading="Front End Development Articles",menu_open=True,
        current_user=current_user,meta_tags=Metatags().set_blog())
    elif path == "back-end":
        return render_template('blog/backend.html',heading="Back End Development Articles", menu_open=True,
                              current_user=current_user, meta_tags=Metatags().set_blog())
    elif path == "api":
        return render_template('blog/api.html',heading="API Development Articles",menu_open=True,
        current_user=current_user,meta_tags=Metatags().set_blog())
    else:
        return render_template('404.html',heading="Page Not Found",menu_open=True,
        current_user=current_user,meta_tags=Metatags().set_blog())

@blog_bp.route('/learn-more/<path:path>', methods=['GET'])
@logged_user
def learn_more(current_user,path):
    get_flashed_messages()
    if path == "backend-development":
        return render_template('learnmore/backend.html',heading="Learn More Back End Development",
        current_user=current_user,menu_open=True,meta_tags=Metatags().set_learn_backend())
    elif path == "frontend-development":
        return render_template('learnmore/frontend.html',heading="Learn More Front End Development",
        current_user=current_user,menu_open=True,meta_tags=Metatags().set_learn_frontend())
    else:
        return render_template("404.html", heading="Page Not Found", 
        current_user=current_user,meta_tags=Metatags().set_home())
