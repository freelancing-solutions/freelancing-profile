import uuid
from .. import db
from ..library.utils import timestamp, const, replace_html
from sqlalchemy.event import listen


class Post(db.Model):
    __bind_key__ = "blog"
    _post_id = db.Column(db.String(const.uuid_len), primary_key=True)
    _uid = db.Column(db.String(const.uuid_len), unique=False, nullable=False)
    _title = db.Column(db.String(const.title_len), nullable=False, unique=True)
    _article = db.Column(db.Text, nullable=False)
    _category = db.Column(db.String, nullable=False)
    _link = db.Column(db.String(const.link_len), nullable=True)
    _draft = db.Column(db.String(const.draft_len), nullable=True, default="")
    _is_published = db.Column(db.Boolean, default=False)
    _date_created = db.Column(db.Integer, default=timestamp())
    _last_modified = db.Column(db.Integer, default=timestamp(), onupdate=timestamp())
    _date_published = db.Column(db.Integer, default=0)

    @property
    def uid(self) -> str:
        return self._uid

    @uid.setter
    def uid(self, uid) -> None:
        if uid is None:
            raise ValueError('UID cannot be Null')
        if not isinstance(uid, str):
            raise TypeError('UID can only be a string')
        self._uid = uid

    @property
    def post_id(self) -> str:
        return self._post_id
    
    @post_id.setter
    def post_id(self, post_id: str) -> None:
        if post_id is None:
            raise ValueError('Post ID cannot be Null')
        if not isinstance(post_id, str):
            raise TypeError('Post ID can only be a string')
        self._post_id = post_id

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, title: str) -> None:
        if title is None:
            raise ValueError('Title cannot be Null')
        if not isinstance(title, str):
            raise TypeError('Title can only be a string')
        self._title = title

    @property
    def article(self) -> str:
        return self._article

    @article.setter
    def article(self, article: str) -> None:
        if article is None:
            raise ValueError('article cannot be Null')
        if not isinstance(article, str):
            raise TypeError('article can only be a string')
        self._article = article

    @property
    def draft(self) -> str:
        return self._draft

    @draft.setter
    def draft(self, draft: str) -> None:
        if draft is None:
            raise ValueError('draft cannot be Null')
        if not isinstance(draft, str):
            raise TypeError('draft can only be a string')
        self._draft = draft

    @property
    def link(self) -> str:
        return self._link

    @link.setter
    def link(self, link: str) -> None:
        if link is None:
            raise ValueError('link cannot be Null')
        if not isinstance(link, str):
            raise TypeError('link can only be a string')
        self._link = link

    @property
    def is_published(self) -> bool:
        return self._is_published

    @is_published.setter
    def is_published(self, ispublished: bool) -> None:
        if not isinstance(ispublished, bool):
            raise TypeError('Invalid Argument is_published is Boolean')
        self._is_published = ispublished

    @property
    def date_published(self) -> int:
        return self._date_published

    @date_published.setter
    def date_published(self, date_published: int) -> None:
        if date_published is None:
            raise ValueError('Date Published is Null')
        if not isinstance(date_published, int):
            raise TypeError('Date Published can only be Integer')

        self._date_published = date_published

    @property
    def last_modified(self) -> int:
        return self._last_modified

    @last_modified.setter
    def last_modified(self, last_modified) -> None:
        if last_modified is None:
            raise ValueError('Last Modified cannot be Null')
        if not isinstance(last_modified, int):
            raise TypeError('last_modified can only be an integer')
        self._last_modified = last_modified

    @property
    def date_created(self) -> int:
        return self._date_created

    @date_created.setter
    def date_created(self, date_created) -> None:
        if date_created is None:
            raise ValueError('date created cannot be Null')
        if not isinstance(date_created, int):
            raise TypeError('date created can only be an integer')

        self._date_created = date_created

    @staticmethod
    def create_draft(article) -> str:
        return article[:const.draft_len] if len(article) > const.draft_len else article

    @staticmethod
    def create_link(title) -> str:
        return '/blog/posts/{}'.format(title[:const.link_len].replace(" ", "_")) if len(title) > const.link_len \
            else '/blog/posts/'.format(title.replace(" ", "_"))

    def __init__(self, uid: str, title: str, article: str, ispublished: bool = False, link: str = None,
                 draft: str = None):
        super(Post, self).__init__()
        self.post_id = str(uuid.uuid4())
        self.uid = uid
        self.title = title.strip()
        self.article = article.strip()
        self.link = link if not(link is None) else self.create_link(title=title)
        self.draft = draft if not(draft is None) else self.create_draft(article=replace_html(self.article))
        self.is_published = ispublished
        self.date_published = timestamp() if self.is_published else 0
        self.date_created = timestamp()
        self.last_modified = timestamp()


class Categories(db.Model):
    __bind_key__ = "blog"
    _category_id = db.Column(db.String(const.uuid_len), primary_key=True)
    _category_name = db.Column(db.String(const.names_len), nullable=False, unique=True)
    _category_description = db.Column(db.String(const.names_len), nullable=False, unique=True)

    @property
    def category_id(self) -> str:
        return self._category_id

    @category_id.setter
    def category_id(self, category_id) -> None:
        if category_id is None:
            raise ValueError('category_id cannot be Null')
        if not isinstance(category_id, str):
            raise TypeError('category id can only be a str')

        self._category_id = category_id

    @property
    def category_name(self) -> str:
        return self._category_id

    @category_name.setter
    def category_name(self, category_name) -> None:
        if category_name is None:
            raise ValueError('category_name cannot be Null')
        if not isinstance(category_name, str):
            raise TypeError('category_name can only be a string')
        self._category_name = category_name

    @property
    def category_description(self) -> str:
        return self._category_description

    @category_description.setter
    def category_description(self, category_description) -> None:
        if category_description is None:
            raise ValueError('category_description cannot be Null')
        if not isinstance(category_description, str):
            raise TypeError('category_description can only be a string')
        self._category_description = category_description

    def __init__(self, category_name, category_description) -> None:
        self.category_id = str(uuid.uuid4())
        self.category_name = category_name
        self.category_description = category_description

    def __str__(self):
        return "<Categories category_name: {}, category_description: {}".format(self.category_name,
                                                                                self.category_description)

    def __repr__(self):
        return self.__str__()


def update_link(target, value, oldvalue, initiator):
    # if value is not None:
    #     target.link = value[:const.link_len].replace(" ", "-")
    #     return value
    print("Initiator : {}".format(initiator))
    print("target : {}".format(target))
    print("oldvalue: {}".format(oldvalue))
    return value


def update_draft(target, value, oldvalue, initiator):
    # if value is not None:
    #     target.draft = value[:const.draft_len]
    #     return value
    print("Initiator : {}".format(initiator))
    print("target : {}".format(target))
    print("oldvalue: {}".format(oldvalue))
    return value


def is_published(target, value, oldvalue, initiator):
    # if value is True:
    #     target.date_published = timestamp()
    #     return value
    print("Initiator : {}".format(initiator))
    print("target : {}".format(target))
    print("oldvalue: {}".format(oldvalue))
    return value


listen(Post._title, 'set', update_link, retval=True,)
listen(Post._article, 'set', update_draft, retval=True)
listen(Post._is_published, 'set', is_published, retval=True)


