from flask import render_template, request, Blueprint, get_flashed_messages, url_for, current_app, jsonify
from sqlalchemy.exc import OperationalError, InvalidRequestError

from .models import Post
from .. import cache, db
from ..app_settings_store.settingsModels import SiteMapsModel
from ..library import Metatags, logged_user, token_required
from ..library.utils import const

blog_bp = Blueprint('blog', __name__, static_folder="static", template_folder="templates")


# Blog Routes
@blog_bp.route('/tech-articles', methods=['GET'])
@cache.cached(timeout=const.cache_timeout_hour)
@logged_user
def blog(current_user: any) -> tuple:
    get_flashed_messages()
    if request.method == "GET":
        return render_template('blog.html', heading="Blog", menu_open=True,
                               current_user=current_user, meta_tags=Metatags().set_blog()), 200
    else:
        return render_template('404.html', heading="Page Not Found", menu_open=True,
                               current_user=current_user, meta_tags=Metatags().set_blog()), 200


@blog_bp.route('/tech-articles/articles/<path:path>')
@cache.cached(timeout=const.cache_timeout_hour)
@logged_user
def frontend_articles(current_user: any, path: str) -> tuple:
    get_flashed_messages()
    if request.method == "GET":
        if path == "service-workers/custom-service-worker-with-push-notifications":
            title: str = "Custom Service Worker with push Notifications"
            template: str = 'blog/frontend_articles/service_workers.html'
            return render_template(template, current_user=current_user, heading=title,
                                   meta_tags=Metatags().set_blog()), 200

        elif path == "python/testing/using-pytest-for-alchemy-models":
            title: str = "Using Pytest to test Alchemy Models"
            template: str = 'blog/backend_articles/pytest-alchemy-models.html'
            return render_template(template, current_user=current_user, heading=title,
                                   meta_tags=Metatags().set_blog()), 200

        return render_template('404.html', heading="Page Not Found", menu_open=True,
                               current_user=current_user, meta_tags=Metatags().set_blog()), 404


@blog_bp.route('/tech-articles/categories/<path:path>', methods=['GET'])
@cache.cached(timeout=const.cache_timeout_hour)
@logged_user
def blog_categories(current_user: any, path: str) -> tuple:
    get_flashed_messages()
    if path == "front-end":
        title: str = "Front End Development Articles"
        template: str = 'blog/frontend.html'
        return render_template(template, heading=title, menu_open=True, current_user=current_user,
                               meta_tags=Metatags().set_blog()), 200
    elif path == "back-end":
        title: str = 'Back End Development Articles'
        template: str = 'blog/backend.html'
        return render_template(template, heading=title, menu_open=True, current_user=current_user,
                               meta_tags=Metatags().set_blog()), 200
    elif path == "api":
        title: str = 'API Development Articles'
        template: str = 'blog/api.html'
        return render_template(template, heading=title, menu_open=True, current_user=current_user,
                               meta_tags=Metatags().set_blog()), 200
    else:
        title: str = "Page not Found"
        return render_template('404.html', heading=title, menu_open=True,
                               current_user=current_user, meta_tags=Metatags().set_blog()), 404


@blog_bp.route('/learn-more/<path:path>', methods=['GET'])
@cache.cached(timeout=const.cache_timeout_hour)
@logged_user
def learn_more(current_user: any, path: str) -> tuple:
    get_flashed_messages()
    if path == "backend-development":
        title: str = 'Learn More Back End Development'
        template: str = 'learnmore/backend.html'
        return render_template(template, heading=title, current_user=current_user, menu_open=True,
                               meta_tags=Metatags().set_learn_backend()), 200
    elif path == "frontend-development":
        title: str = 'Learn More Front End Development'
        template: str = 'learnmore/frontend.html'
        return render_template(template, heading=title, current_user=current_user, menu_open=True,
                               meta_tags=Metatags().set_learn_frontend()), 200
    else:
        return render_template("404.html", heading="Page Not Found",
                               current_user=current_user, meta_tags=Metatags().set_home()), 404


# Dynamic Blog Pages

@blog_bp.route('/blog/editor', methods=['GET', 'POST'])
@token_required
def blog_editor(current_user):
    if request.method == "GET":
        if current_user and current_user.uid:
            print(current_user)
            return render_template('blog/editor.html', heading='Blog Editor', current_user=current_user,
                                   meta_tags=Metatags().set_blog()), 200
        else:
            message: str = """
            You are currently not Authorized to view this resource please login to continue
            """
            return render_template('error.html', heading="Not Authorized", message=message, code=401,
                                   current_user=current_user, meta_tags=Metatags().set_blog())
    else:
        if current_user and current_user.uid:
            print(current_user)
            blog_post_detail = request.get_json()
            if 'title' in blog_post_detail and not(blog_post_detail['title'] == ""):
                title: str = blog_post_detail['title']
            else:
                return jsonify({'status': 'failure', 'message': 'title cannot be Null'}), 500

            if 'article' in blog_post_detail and not(blog_post_detail['article'] == ""):
                article: str = blog_post_detail['article']
            else:
                return jsonify({'status': 'failure', 'message': 'article cannot be Null'}), 500

            if 'draft' in blog_post_detail and not(blog_post_detail['draft'] == ""):
                draft: str = blog_post_detail['draft']
            else:
                return jsonify({'status': 'failure', 'message': 'article cannot be Null'}), 500

            if 'is_published' in blog_post_detail and not(blog_post_detail['is_published'] == ""):
                is_published: bool = blog_post_detail['is_published']
            else:
                return jsonify({'status': 'failure', 'message': 'is_published cannot be Null'}), 500
            try:
                post_found_list = Post.query.filter_by(title=title.strip()).all()
                if len(post_found_list) > 0:
                    return jsonify({'status': 'failure', 'message': 'post already exists please use a different title'}), 500

                post_instance = Post(uid=current_user.uid, title=title, draft=draft, article=article,
                                     ispublished=is_published)
                blog_sitemap = SiteMapsModel(resource_name=current_app.config['BLOGGING_SITEMAP'], link=post_instance.link)
                db.session.add(post_instance)
                db.session.add(blog_sitemap)
                db.session.commit()
                return jsonify({'status': 'success', 'message': 'successfully created post'}), 200
            
            except OperationalError as e:
                db.session.rollback()
                db.session.commit()
                return jsonify({'status': 'failure', 'message': 'Database Error while creating post'}), 500
            except InvalidRequestError as e:
                db.session.rollback()
                db.session.commit()
                return jsonify({'status': 'failure', 'message': 'Database Error while creating post'}), 500
        else:
            return jsonify({'status': 'failure', 'message': 'user not logged in'}), 500

