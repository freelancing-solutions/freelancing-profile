from flask import render_template, request, Blueprint
from ..library import Metatags

blog_bp = Blueprint('blog', __name__)


###########################################################################################################
# Blog Routes
@blog_bp.route('/blog', methods=['GET'])
def blog():
    if request.method == "GET":
        return render_template('blog.html', heading="Blog", menu_open=True, meta_tags=Metatags().set_blog())
    else:
        pass


@blog_bp.route('/blog/categories/<path:path>', methods=['GET'])
def blog_categories(path):
    if path == "front-end":
        # TODO- Fetch Front end Posts
        return render_template('blog/frontend.html', heading="Front End Development Articles", menu_open=True,
                               meta_tags=Metatags().set_blog())
    elif path == "back-end":
        return render_template('blog/backend.html', heading="Back End Development Articles", menu_open=True,
                               meta_tags=Metatags().set_blog())
    elif path == "api":
        return render_template('blog/api.html', heading="API Development Articles", menu_open=True,
                               meta_tags=Metatags().set_blog())
    else:
        return render_template('404.html', heading="Page Not Found", menu_open=True,
                               meta_tags=Metatags().set_blog())


@blog_bp.route('/learn-more/<path:path>', methods=['GET'])
def learn_more(path):
    if path == "backend-development":
        return render_template('learnmore/backend.html',
                               heading="Learn More Back End Development",
                               menu_open=True,
                               meta_tags=Metatags().set_learn_backend())
    elif path == "frontend-development":
        return render_template('learnmore/frontend.html',
                               heading="Learn More Front End Development",
                               menu_open=True,
                               meta_tags=Metatags().set_learn_frontend())
    else:
        return render_template("404.html", heading="Page Not Found", meta_tags=Metatags().set_home())

