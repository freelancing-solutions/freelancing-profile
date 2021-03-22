from flask import  render_template, request, Blueprint, get_flashed_messages, url_for
from ..library import Metatags, logged_user
from flask_blogging.sqlastorage import Post, Tag

blog_bp = Blueprint('blog', __name__, static_folder="static", template_folder="templates")

###########################################################################################################


@blog_bp.route('/blog/home', methods=['GET'])
def blog_index():
    return render_template(url_for('blogging.index'))


@blog_bp.route('/blog/post/<path:post_id>', methods=['GET'])
def blog_page_by_id(post_id):
    return render_template(url_for('blogging.page_by_id', post_id=post_id))


@blog_bp.route('/blog/posts/tag/<path:tag_name>', methods=['GET'])
def blog_posts_by_tag(tag_name):
    return render_template(url_for('blogging.posts_by_tag', tag=tag_name))


@blog_bp.route('/blog/posts/author/<path:user_id>', methods=['GET'])
def blog_posts_by_author(user_id):
    return render_template(url_for('blogging.posts_by_tag', user_id=user_id))


@blog_bp.route('/blog/editor', methods=['GET', 'POST'])
def blog_post_editor():
    return render_template(url_for('blogging.editor'))


@blog_bp.route('/blog/post/delete/<path:post_id>', methods=['POST'])
def blog_post_delete(post_id):
    return render_template(url_for('blogging.delete', post_id=post_id))


@blog_bp.route('/blog/sitemap.xml', methods=['GET'])
def blog_sitemap():
    return render_template(url_for('blogging.sitemap'))


@blog_bp.route('/blog/feed', methods=['GET'])
def blog_feed():
    return render_template(url_for('blogging.feed'))


# Blog Routes
@blog_bp.route('/tech-articles', methods=['GET'])
@logged_user
def blog(current_user):
    get_flashed_messages()
    if request.method == "GET":
        return render_template('blog.html', heading="Blog", menu_open=True,
                               current_user=current_user, meta_tags=Metatags().set_blog())
    else:
        return render_template('404.html', heading="Page Not Found", menu_open=True,
                               current_user=current_user, meta_tags=Metatags().set_blog())


@blog_bp.route('/tech-articles/articles/<path:path>')
@logged_user
def frontend_articles(current_user, path):
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


@blog_bp.route('/tech-articles/categories/<path:path>', methods=['GET'])
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
def learn_more(current_user, path):
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
