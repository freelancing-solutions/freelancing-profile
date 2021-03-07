# import unittest
from .. import db, create_app
from flask import current_app, url_for
from ..library import config


def test_blog_routes():
    if not current_app:
        app = create_app(config_class=config.TestingConfig)
        app.app_context().push()
    else:
        app = current_app
    app.testing = True
    with app.app_context():        
        with app.test_client(use_cookies=True) as test_client:
            assert test_client.get('/blog'), "could not access blog home page"
            # assert test_client.get(url_for('blog.blog')), "could not access blog home page through url-for method"

            assert test_client.get("/blog/categories/front-end"), "could not retrived Blog front end page"
            assert test_client.get("/blog/categories/back-end"), "Could not retrieve Blog back end page"
            assert test_client.get("/blog/categories/api"), "Could not retrieve blog API page"
            assert test_client.get("/blog/categories/404"), "Could not retrieve blog 404 page"

            # assert test_client.get(url_for('blog.blog_categories', path="front-end")), "Could not retrieve blog front end page using url_for method"
            # assert test_client.get(url_for('blog.blog_categories', path="back-end")), "Could not access blog back-end route by using url_for method"
            # assert test_client.get(url_for('blog.blog_categories', path="api")), "Could not access blog api route through the url_for method"
            # assert test_client.get(url_for('blog.blog_categories', path="xxx")), "Not returning 404 not found page for inaccessible pages using url_for method"

            assert test_client.get("/learn-more/backend-development"), "Could not retrieve learn more back-end page"
            assert test_client.get("/learn-more/frontend-development"), "Could not access learn more front-end development"
            assert test_client.get("/learn-more/xxx"), "learn more route breaks and dont return 404 when accessed incorrectly"