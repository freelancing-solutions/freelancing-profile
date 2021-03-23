from .. import db
from flask import escape
from ..library.utils import timestamp, create_id, const
import time
import uuid
from sqlalchemy.event import listen


class Post(db.Model):
    __bind_key__ = "blog"
    _post_id = db.Column(db.String(const.uuid_len), primary_key=True)
    _uid = db.Column(db.String(const.uuid_len), unique=False, nullable=False)
    _title = db.Column(db.String(const.title_len), nullable=False)
    _article = db.Column(db.Text, nullable=False)
    _link = db.Column(db.String(const.link_len), nullable=True)
    _last_modified = db.Column(db.Integer, onupdate=timestamp())
    _date_created = db.Column(db.Integer, default=timestamp())
    _draft = db.Column(db.String(const.draft_len), nullable=True, default="")
    _is_published = db.Column(db.Boolean, default=False)
    _date_published = db.Column(db.Integer, default=0)


    @property
    def post_id(self):
        return self._post_id
    
    @post_id.setter
    def post_id(self, post_id):
        if post_id is None:
            raise ValueError('Post ID cannot be Null')
        if not isinstance(post_id, str):
            raise TypeError('Post ID can only be a string')
        self._post_id = post_id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        if title is None:
            raise ValueError('Title cannot be Null')
        if not isinstance(title, str):
            raise TypeError('Title can only be a string')
        self._title = title

    @property
    def article(self):
        return self._article

    @article.setter
    def article(self, article):
        if article is None:
            raise ValueError('article cannot be Null')
        if not isinstance(article, str):
            raise TypeError('article can only be a string')
        self._article = article

    @property
    def draft(self):
        return self._draft

    @draft.setter
    def draft(self, draft):
        if draft is None:
            raise ValueError('draft cannot be Null')
        if not isinstance(draft, str):
            raise TypeError('draft can only be a string')
        self._draft = draft

    @property
    def link(self):
        return self._link

    @link.setter
    def link(self, link):
        if link is None:
            raise ValueError('link cannot be Null')
        if not isinstance(link, str):
            raise TypeError('link can only be a string')
        self._link = link

    @property
    def is_published(self):
        return self._is_published

    @is_published.setter
    def is_published(self, is_published):
        if not isinstance(is_published, bool):
            raise TypeError('Invalid Argument is_published is Boolean')
        self._is_published = is_published


    @property
    def date_published(self):
        return self._date_published

    @date_published.setter
    def date_published(self, date_published):
        if date_published is None:
            raise ValueError('Date Published is Null')
        if not isinstance(date_published, int):
            raise TypeError('Date Published can only be Integer')

        self._date_published = date_published

    def __init__(self, uid, title, article, is_published=False, link=None, draft=None):
        self.post_id = str(uuid.uuid4())
        self.uid = uid
        self.title = title
        self.article = article
        self.is_published = is_published
        if link:
            self.link = link
        if draft:
            self.draft = draft

        super(Post, self).__init__()


def update_link(target, value, oldvalue, initiator):
    if value is not None:
        return value[:const.link_len].replace(" ", "-")


def update_draft(target, value, oldvalue, initiator):
    if value is not None:
        return value[:const.draft_len]


def is_published(target, value, oldvalue, initiator):
    if value is True:
        target.date_published = timestamp()


listen(Post.title, 'set', update_link, retval=True)
listen(Post.article, 'set', update_draft, retval=True)
listen(Post.is_published, 'set', is_published, retval=True)


