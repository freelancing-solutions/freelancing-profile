from .. import db
from ..library.utils import timestamp, create_id, const
import time
import uuid


class AmountMixin(object):
    _currency = db.Column(db.String(const.currency_len), unique=False, nullable=False, default="$")
    _amount = db.Column(db.Integer, unique=False, nullable=False, default=0)

    @property
    def currency(self):
        return self._currency

    @currency.setter
    def currency(self, currency):
        if currency is None:
            raise ValueError('Currency cannot be Null')
        if currency not in const.currency_list:
            raise ValueError('Invalid Currency')

        self._currency = currency

    @property
    def amount(self) -> int:
        return self._amount

    @amount.setter
    def amount(self, amount):
        if amount is None:
            raise ValueError('Amount cannot be null')
        if not isinstance(amount, int):
            raise TypeError('Amount can only be an integer')
        self._amount = amount


# TODO try using mixin for amount and currency
class PaymentModel(AmountMixin, db.Model):
    """
        to access transactions use backref : transactions -> a list
        to access the freelancejob this refers to use backref : freelancejob
        to access user use backref : user
    """
    _payment_id = db.Column(db.String(const.uuid_len), primary_key=True, unique=True)
    _total_paid = db.Column(db.Integer, nullable=False, default=0)
    _balance = db.Column(db.Integer, nullable=False, default=0)
    _last_transaction_date = db.Column(db.Integer, nullable=False, default=0)
    _is_fully_paid = db.Column(db.Boolean, nullable=False, default=False)
    _time_fully_paid = db.Column(db.Integer, nullable=False, default=0)
    _time_created = db.Column(db.Integer, nullable=False, default=int(float(time.time() * 1000)))
    _uid = db.Column(db.String(const.uuid_len), db.ForeignKey('user_model._uid'), unique=False, nullable=False)
    _project_id = db.Column(db.String(const.uuid_len), db.ForeignKey('freelance_job_model._project_id'), unique=True,
                            nullable=False)
    _transactions = db.relationship('TransactionModel', backref=db.backref('payment', lazy=True))

    @property
    def transactions(self):
        return self._transactions

    @transactions.setter
    def transactions(self, transaction):
        if isinstance(self._transactions, list):
            self._transactions.append(transaction)
        else:
            pass

    @property
    def total_paid(self):
        return self._total_paid

    @total_paid.setter
    def total_paid(self, total_paid):
        if total_paid is None:
            raise ValueError('Total Paid cannot be Null')
        if not isinstance(total_paid, int):
            raise TypeError('Total paid can only be an Integer')

        self._total_paid = total_paid

    @property
    def balance(self):
        return self._balance

    def set_balance(self):
        self._balance = self.amount - self.total_paid

    @property
    def is_fully_paid(self):
        return self._is_fully_paid

    def set_is_fully_paid(self):
        if self.total_paid >= self.amount:
            self._is_fully_paid = True
        else:
            self._is_fully_paid = False

    @property
    def last_transaction_date(self):
        return self._last_transaction_date

    @last_transaction_date.setter
    def last_transaction_date(self, last_transaction_date):
        if last_transaction_date is None:
            raise ValueError('Last Transaction Date is Null')
        if not isinstance(last_transaction_date):
            raise TypeError('Last Transaction Date can only be an integer')
        self._last_transaction_date = last_transaction_date

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

    @time_fully_paid.setter
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
        self.total_paid = 0
        self.set_balance()
        self.set_is_fully_paid()
        # NOTE: transactions array should be empty at initializing
        super(PaymentModel, self).__init__()

    def __eq__(self, payment):
        """
            if payment_id are equal then consider the entire thing to be equal
        """
        if payment.payment_id == self.payment_id and (payment.uid == self.uid) and (payment.amount == self.amount):
            return True
        return False

    @classmethod
    def add_transaction(cls, payment_id, transaction):
        payment_instance = PaymentModel.query.filter_by(_payment_id=payment_id).first()
        payment_instance.transactions.append(transaction)
        db.session.update(payment_instance)
        db.session.commit()


class TransactionModel(AmountMixin, db.Model):
    """
        verification_token should be sent as part of the eft transaction [header]
        so that once verification information is sent, the token can be used to verify that
        the transaction succeeded and comes from here
    """
    # NOTE Payment Method paypal, credit-card, eft, crypto-currency
    _transaction_id = db.Column(db.String(const.uuid_len), primary_key=True, unique=True)
    _payment_id = db.Column(db.String(const.uuid_len), db.ForeignKey('payment_model._payment_id'), unique=False,
                            nullable=False)
    _method = db.Column(db.String(const.transaction_method_len), unique=False, nullable=False, default="paypal")
    _time_paid = db.Column(db.Integer, nullable=False, default=0)
    _verification_token = db.Column(db.String(const.id_len), nullable=False, default=create_id())
    _is_verified = db.Column(db.Boolean, nullable=False, default=False)
    _time_verified = db.Column(db.Integer, nullable=False, default=0)
    _payment = db.relationship('PaymentModel', backref=db.backref('transactions', lazy=True))

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
    def payment_id(self) -> str:
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
        if method not in ['paypal', 'credit-card', 'eft', 'crypto-currency']:
            raise ValueError('Invalid Payment Method')

        self._method = method

    @property
    def time_paid(self) -> int:
        return self._time_paid

    @time_paid.setter
    def time_paid(self, time_paid):
        if time_paid is None:
            raise ValueError('Time Paid cannot be Null')
        if not isinstance(time_paid, int):
            raise TypeError('Time paid can only be an integer')
        self._time_paid = time_paid

    @property
    def time_verified(self) -> int:
        return self._time_verified

    @time_verified.setter
    def time_verified(self, time_verified):
        if time_verified is None:
            raise ValueError('Time Paid cannot be Null')
        if not isinstance(time_verified, int):
            raise TypeError('Time paid can only be an integer')
        self._time_verified = time_verified

    @property
    def is_verified(self) -> bool:
        return self._is_verified

    @is_verified.setter
    def is_verified(self, is_verified):
        if not isinstance(is_verified, bool):
            raise TypeError('is verified can only be a boolean')

        self._is_verified = is_verified

    def __init__(self, payment_id, method, currency, amount):
        self.transaction_id = str(uuid.uuid4())
        self.payment_id = payment_id
        self.method = str(method).lower()
        self.amount = int(amount)
        self.currency = currency
        self.time_paid = timestamp()
        super(TransactionModel, self).__init__()

    def __eq__(self, value) -> bool:
        """
            :type value: self
            :param value:
            :return: bool
        """
        if (value.transaction_id == self.transaction_id) and (value.payment_id == self.payment_id):
            return True
        return False

    def __repr__(self) -> str:
        return "<Transaction Method: {}, Amount: {}{}, Time Paid: {}, Verified: {} />".format(self.method,
                                                                                              self.currency,
                                                                                              self.amount,
                                                                                              self.time_paid,
                                                                                              self._is_verified)

    # call this method to verify payment
    def verify(self):
        payment_instance = PaymentModel.query.filter_by(_payment_id=self.payment_id).first()
        if payment_instance:
            self.is_verified = True
            self.time_verified = timestamp()
            payment_instance.total_paid += self.amount
            payment_instance.set_balance()
            payment_instance.set_is_fully_paid()
            db.session.add(self)
            db.session.update(payment_instance)
            db.session.commit()
            return True
        else:
            return False



