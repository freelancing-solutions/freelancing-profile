from flask import url_for
from sqlalchemy.exc import OperationalError

from .. import db
from ..library.utils import const, create_id
import requests


# add a javascript module to gather client data
class ClientModel(db.Model):
    __bind_key__ = "settings"
    client_id = db.Column(db.String(const.id_len), primary_key=True)
    uid = db.Column(db.String(const.uuid_len), nullable=True)
    ip_address = db.Column(db.String(const.ip_length), unique=False, default="127.0.0.1")
    browser = db.Column(db.String(const.names_len), unique=False)
    os = db.Column(db.String(const.names_len), unique=False)
    device = db.Column(db.String(const.names_len), unique=False)

    def __init__(self, uid, ip_address, browser, os, device):
        super(ClientModel, self).__init__()
        self.client_id = create_id()
        self.uid = uid
        self.ip_address = ip_address
        self.browser = browser
        self.os = os
        self.device = device

    def __bool__(self):
        return False if self.client_id is None else True


class StatsLoggerModel(db.Model):
    __bind_key__ = "settings"
    app_instance_id = db.Column(db.String(const.id_len), primary_key=True)
    server_started_time = db.Column(db.Integer, default=0)
    requests_count = db.Column(db.Integer, default=0)
    static_requests = db.Column(db.Integer, default=0)
    docs_requests = db.Column(db.Integer, default=0)
    errors = db.Column(db.Integer, default=0)
    highest_latency = db.Column(db.Float, default=0.0)
    unique_visitor = db.Column(db.Float, default=0.0)
    return_visitor = db.Column(db.Float, default=0.0)
    page_views = db.Column(db.Integer, default=0)

    def __init__(self, app_instance_id, server_started_time, requests_count, static_requests, docs_requests, errors,
                 highest_latency, unique_visitor, return_visitor, page_views):
        super(StatsLoggerModel, self).__init__()
        self.app_instance_id = app_instance_id
        self.server_started_time = server_started_time
        self.requests_count = requests_count
        self.static_requests = static_requests
        self.docs_requests = docs_requests
        self.errors = errors
        self.highest_latency = highest_latency
        self.unique_visitor = unique_visitor
        self.return_visitor = return_visitor
        self.page_views = page_views


class ClientConfigModel(db.Model):
    __bind_key__ = "settings"
    client_id = db.Column(db.String(const.uuid_len), primary_key=True)


class APPConfigModel(db.Model):
    __bind_key__ = "settings"
    app_name = db.Column(db.String(const.names_len), primary_key=True)


class BlogSettingsModel(db.Model):
    __bind_key__ = "settings"
    blog_name = db.Column(db.String(const.names_len), primary_key=True)


class SiteMapsModel(db.Model):
    __bind_key__ = "settings"
    id = db.Column(db.String(const.uuid_len), primary_key=True)
    resource_name = db.Column(db.String(const.names_len), unique=False, nullable=False)
    link = db.Column(db.String(const.link_len), unique=True, nullable=False)

    def __init__(self, resource_name, link):
        self.id = create_id()
        self.resource_name = resource_name
        self.link = link

    def __bool__(self):
        return False if self.id is None else True

    @staticmethod
    def check_if_all_exist():
        """
            tests all links in database and removes links which do not exist
        """
        try:
            sitemap_links = SiteMapsModel.query().all()
            for sitemap in sitemap_links:
                try:
                    url = url_for('main.home')
                    response = requests.get(url=url+sitemap.link)
                    if not response.ok:
                        db.session.delete(sitemap)

                except ConnectionError as e:
                    db.session.delete(sitemap)

            db.session.commit()
        except OperationalError as e:
            pass

    @staticmethod
    def return_all_dynamic_links() -> list:
        """
            returns all dynamic sitemap links, this includes dynamic blog posts/ github repos/ and gists,
        :return:
        """
        try:
            print('dynamic links ')
            print([sitemap.link for sitemap in SiteMapsModel.query.order_by(SiteMapsModel.link).all()])
            return [sitemap.link for sitemap in SiteMapsModel.query.order_by(SiteMapsModel.link).all()]
        except OperationalError as e:
            return []
