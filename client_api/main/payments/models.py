from .. import db
from flask import current_app

class PaymentModel(db.Model):
    """
        to access transactions use backref : transactions -> a list
        to access the freelancejob this refers to use backref : freelancejob
        to access user use backref : user
    """
    _payment_id = db.Column(db.String(36), primary_key=True, unique=True)
    _amount = db.Column(db.Integer, unique=False, nullable=False, default=0)
    _is_fully_paid = db.Column(db.Boolean, nullable=False, default=False)
    _time_fully_paid = db.Column(db.Integer, nullable=False, default=0)
    _time_created = db.Column(db.Integer, nullable=False, default=int(float(time.time() * 1000)))
    # _user = db.relationship('UserModel', backref=db.backref('freelancejobs', lazy=True))
    _uid = db.Column(db.String(36),db.ForeignKey('user_model._uid'),unique=False, nullable=False)
    _project_id = db.Column(db.String(36),db.ForeignKey('freelance_job_model._project_id'),unique=True, nullable=False)
    _transactions = db.relationship('TransactionModel', backref=db.backref('payment', lazy=True)

    @property
    def payment_id(self) -> str:
        return self._payment_id

    @payment_id.setter
    def payment_id(self, payment_id):
        if payment_id is not None:
            raise ValueError('Payment ID cannot be Null')
        if not isinstance(payment_id, str):
            raise TypeError('Payment ID can only be a string')

        self._payment_id = payment_id

    @property
    def uid(self) -> str:
        return self._uid

    @uid.setter
    def uid(self, uid):
        if uid is None:
            raise ValueError('UID cannot be null')
        if not isinstance(uid, str):
            raise TypeError('UID can only be a string')

        self._uid = uid

    @property
    def project_id(self) -> str:
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        if project_id is None:
            raise ValueError('project id cannot be null')

        if not isinstance(project_id, str):
            raise TypeError('project_id can only be a str')

        self._project_id = project_id

    @property
    def amount(self) -> int:
        return self._amount

    @amount.setter
    def amount(self,amount):
        if amount is None:
            raise ValueError('Amount cannot be null')

        if not isinstance(amount, int):
            raise TypeError('Amount can only be an integer')

        self._amount = amount

    @property
    def is_fully_paid(self) -> bool:
        return self._is_fully_paid

    @is_fully_paid.setter
    def is_fully_paid(self, is_fully_paid):
        if not isinstance(is_fully_paid, bool):
            raise TypeError('is fully paid can only be a Boolean')
        self._is_fully_paid = is_fully_paid

    @property
    def time_created(self) -> int:
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        if time_created is None:
            raise ValueError('Time created can not be Null')

        if not isinstance(time_created, int):
            raise TypeError('Time created can only be an Integer')

        self._time_created = time_created

    @property
    def time_fully_paid(self) -> int:
        return self._time_fully_paid

    @time_fully_paid
    def time_fully_paid(self, time_fully_paid):
        if time_fully_paid is None:
            raise ValueError('Time Fully Paid cannot be Null')

        if not isinstance(time_fully_paid, int):
            raise TypeError('Time Fully Paid can only be an Integer')

        self._time_fully_paid = time_fully_paid

    def __init__(self, uid, project_id, amount):
        self.payment_id = str(uuid.uuid4())
        self.uid = uid
        # project_id of the freelance_job this payment refers to
        self.project_id = project_id
        self.amount = amount
        # NOTE: transactions array should be empty at initializing
        super(PaymentModel).__init__()

    def __eq__(self,payment):
        """
            if payment_id are equal then consider the entire thing to be equal
        """
        if (payment.payment_id == self.payment_id):
            return True
        return False

    @cls
    def add_transaction(cls, payment_id,transaction):
        payment_instance = PaymentModel.query.filter_by(_payment_id=payment_id).first()
        payment_instance._transactions.push(transaction)
        db.session.update(payment_instance)
        db.session.commit()

class TransactionModel(db.Model):
    _transaction_id = db.Column(db.String(36), primary_key=True, unique=True)
    _payment_id = db.Column(db.String(36),db.ForeignKey('payment_model._payment_id'),unique=False, nullable=False)
    #NOTE Payment Method paypal, credit-card, eft, crypto-currency
    _method = db.Column(db.String(16), unique=False, nullable=False, default="paypal")
    _amount = db.Column(db.Integer, unique=False, nullable=False, default=0)
    _time_paid = db.Column(db.Integer, nullable=False, default=0)
    _is_verified = db.Column(db.Boolean, nullable=False, default=False)
    _payment = db.relationship('PaymentModel', backref=('transactions', lazy=True))

    @property
    def transaction_id(self) -> str:
        return self._transaction_id

    @transaction_id.setter
    def transaction_id(self, transaction_id):
        if transaction_id is None:
            raise ValueError('Transaction ID cannot be Null')

        if not isinstance(transaction_id, str):
            raise TypeError('Transaction ID can only be a string')

        self._transaction_id = transaction_id

    @property
    def payment_id(self)-> str:
        return self._payment_id

    @payment_id.setter
    def payment_id(self, payment_id):
        if payment_id is None:
            raise ValueError('Payment Id cannot be Null')

        if not isinstance(payment_id, str):
            raise TypeError('Payment Id can only be a string')
        self._payment_id = payment_id

    @property
    def method(self) -> str:
        return self._method

    @method.setter
    def method(self, method):
        if method not in ['paypal','credit-card','eft','crypto-currency']:
            raise ValueError('Invalid Payment Method')

        self._method = method

    @property
    def amount(self) -> int:
        return self._amount

    @amount.setter
    def amount(self, amount):
        if amount is None:
            raise ValueError('Amount cannot be Null')
        if not isinstance(amount, int):
            raise TypeError('Amount can only be an integer')
        self._amount = amount

        
