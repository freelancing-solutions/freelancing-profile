import time
from flask import request

# TODO- store this values to ndb, and restore them from ndb upon restart
from ..library import timestamp


class StatsLogger:
    server_started_time: int = 0
    requests_count: int = 0
    static_requests: int = 0
    docs_requests: int = 0
    errors: int = 0
    latent_timer: float = 0
    _latency: float = 0
    _highest_latency: float = 0
    unique_visitor: int = 0
    return_visitor: int = 0
    page_views: int = 0

    @property
    def latency(self) -> float:
        return self._latency * 1000

    @latency.setter
    def latency(self, latency) -> None:
        self._latency = latency

    @property
    def highest_latency(self) -> float:
        return self._highest_latency * 1000

    @highest_latency.setter
    def highest_latency(self, highest_latency) -> None:
        self._highest_latency = highest_latency

    def __repr__(self) -> str:
        return "<StatsLogger requests: {}, static: {}, docs: {}".format(
            self.requests_count, self.static_requests, self.docs_requests)

    def __str__(self) -> str:
        return self.__repr__()

    def __dict__(self) -> dict:
        return {
            "server_started_time": self.server_started_time,
            "requests_count": self.requests_count,
            "static_requests": self.static_requests,
            "docs_requests": self.docs_requests,
            "latency": self.latency,
            "highest_latency": self.highest_latency,
            "unique_visitor": self.unique_visitor,
            "return_visitor": self.return_visitor,
            "page_views": self.page_views,
            "errors": self.errors,

        }

    def uptime(self) -> int:
        """
            returns server uptime in milliseconds
        :return: uptime in milliseconds
        """
        return timestamp() - self.server_started_time

    def add_unique_visitor(self) -> bool:
        self.unique_visitor += 1
        return True

    def add_return_visitor(self) -> bool:
        self.return_visitor += 1
        return True

    def add_page_view(self) -> int:
        self.page_views += 1
        return self.page_views

    def response_request_handler(self, response):
        self._latency = time.time() - self.latent_timer
        if self._latency > self._highest_latency:
            self._highest_latency = self._latency
        return response

    def before_request_handler(self):
        self.latent_timer = time.time()
        self.requests_count += 1
        if request.url.__contains__('static'):
            self.static_requests += 1
        else:
            self.docs_requests += 1

    def init_app(self, app, logger_model):
        statistics_model_instance = logger_model.query.limit(1).first()
        if statistics_model_instance and statistics_model_instance.app_instance_id:
            self.server_started_time = timestamp()
            self.requests_count = statistics_model_instance.requests_count
            self.static_requests = statistics_model_instance.static_requests
            self.docs_requests = statistics_model_instance.docs_requests
            self.errors = statistics_model_instance.errors
            self.highest_latency = statistics_model_instance.highest_latency
            self.unique_visitor = statistics_model_instance.unique_visitor
            self.return_visitor = statistics_model_instance.return_visitor
            self.page_views = statistics_model_instance.page_views
        else:
            self.server_started_time = timestamp()
            self.requests_count = 0
            self.static_requests = 0
            self.docs_requests = 0
            self.errors = 0
            self.highest_latency = 0
            self.unique_visitor = 0
            self.return_visitor = 0
            self.page_views = 0

        app.before_request(self.before_request_handler)
        app.after_request(self.response_request_handler)

        return self

