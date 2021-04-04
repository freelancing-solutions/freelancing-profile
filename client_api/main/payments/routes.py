from flask import render_template, request, Blueprint, get_flashed_messages, jsonify
from pymysql import IntegrityError
from sqlalchemy.exc import OperationalError

from ..library import Metatags, token_required, verify_external_auth_token
from ..library.utils import const, timestamp
from .models import PaymentModel, TransactionModel
from jinja2 import TemplateAssertionError, TemplateRuntimeError
from main import db

payments_bp = Blueprint('payments', __name__, template_folder='../templates', static_folder='../static')


@payments_bp.route('/user/payments', methods=['GET', 'POST'])
@token_required
def payments(current_user: any) -> tuple:
    get_flashed_messages()
    if current_user and current_user.uid:
        if request.method == "GET":
            try:
                payments_instance = PaymentModel.query.filter_by(_uid=current_user.uid).first()
            except OperationalError as e:
                return render_template('error.html', heading='Database Error', message='error connecting to database',
                                       meta_tags=Metatags().set_home()), 500

            if payments_instance and payments_instance.payment_id:
                transactions = payments_instance.transactions
            else:
                transactions = []
            # TODO- learn how to access transactions from
            try:
                return render_template('payments.html', heading='Payments', payment=payments_instance,
                                       transactions_list=transactions,
                                       current_user=current_user, meta_tags=Metatags().set_home(), menu_open=True), 200

            except TemplateAssertionError as e:
                return render_template('error.html', heading='Error loading Page', message=e.message,
                                       meta_tags=Metatags().set_home()), 500
            except TemplateRuntimeError as e:
                return render_template('error.html', heading='Error loading Page', message=e.message,
                                       meta_tags=Metatags().set_home()), 500

        else:
            # TODO- need to decide what to do here
            pass

    else:
        message = ''' 
            You are not authorized to view payment information, 
            <a href="{{ url_for('users.login')}}">please consider login in</a>
        '''
        return render_template('error.html', heading='Not Authorized', message=message,
                               meta_tags=Metatags().set_home()), 401


@payments_bp.route('/user/make-payment/<path:path>', methods=['GET', 'POST'])
@token_required
def make_payment(current_user: any, path: str) -> tuple:
    get_flashed_messages()
    if current_user and current_user.uid:
        if request.method == "GET":
            payment_id = path
            try:
                payment_instance = PaymentModel.query.filter_by(_payment_id=payment_id).first()
            except OperationalError as e:
                message = '''
                    Sorry we are unable to locate the payment record referenced
                    however try making payments directly from freelance jobs page
                '''
                return render_template('error.html', heading='Payment Record Not found', message=message,
                                       meta_tags=Metatags().set_home()), 500

            try:
                return render_template('payments/payment.html', heading='Make Payment',
                                       current_user=current_user,
                                       meta_tags=Metatags().set_home(), menu_open=True,
                                       payment_id=payment_id), 200

            except TemplateAssertionError as e:
                return render_template('error.html', heading='Error loading Page', message=e.message,
                                       meta_tags=Metatags().set_home()), 500
            except TemplateRuntimeError as e:
                return render_template('error.html', heading='Error loading Page', message=e.message,
                                       meta_tags=Metatags().set_home()), 500
        else:
            # NOTE: this is where the user is creating the actual transaction
            try:
                payment_details = request.get_json()
            except Exception as e:
                message = '''
                    Error reading your submitted payment information consider enabling javascript on your browser                                         
                '''
                return render_template('error.html', heading='Unable to read payment information', message=message,
                                       meta_tags=Metatags().set_home()), 500

            if 'method' not in payment_details:
                return jsonify({'status': 'failure', 'message': 'There was an error parsing your request'}), 500
            if 'amount' not in payment_details:
                return jsonify({'status': 'failure', 'message': 'There was an error parsing your request'}), 500
            if 'currency' not in payment_details:
                return jsonify({'status': 'failure', 'message': 'There was an error parsing your request'}), 500
            if 'payment_id' not in payment_details:
                return jsonify({'status': 'failure', 'message': 'There was an error parsing your request'}), 500

            amount: int = payment_details['amount']
            currency: str = payment_details['currency']
            payment_id: str = payment_details['payment_id']
            method: str = payment_details['method']

            if amount is None:
                return jsonify({'status': 'failure', 'message': 'Payment amount cannot be Null'}), 500
            if not (currency in const.currency_list):
                return jsonify({'status': 'failure', 'message': 'Invalid Currency'}), 500
            if not (method in const.payment_methods):
                return jsonify({'status': 'failure', 'message': 'Invalid Payment Method'}), 500
            if payment_id is None:
                return jsonify({'status': 'failure', 'message': 'Payment ID cannot be Null'}), 500
            try:
                payment_instance = PaymentModel.query.filter_by(_payment_id=payment_id).first()
            except OperationalError as e:
                return jsonify({'status': 'failure', 'message': 'Database Error please inform admin'}), 500

            if payment_instance and (payment_instance.amount > int(amount)) and (currency == payment_instance.currency):
                try:
                    new_transaction = TransactionModel(payment_id=payment_id, method=method, amount=amount,
                                                       currency=currency)

                    # TODO- first try verifying payment information before you can actually substract payment amount
                    # payment_instance.amount -= int(amount)
                    payment_instance.last_transaction_date = timestamp()
                    payment_instance.transactions = new_transaction
                    db.session.update(payment_instance)
                    # db.session.add(new_transaction)
                    db.session.commit()
                except OperationalError as e:
                    return jsonify({'status': 'failure', 'message': 'Database Error please inform admin'}), 500
                except IntegrityError as e:
                    return jsonify({'status': 'failure', 'message': 'Data Integrity error please inform admin'}), 500

                return jsonify({'status': 'failure', 'message': 'Successfully created new transaction'}), 200
            else:
                return jsonify({'status': 'failure', 'message': 'Database Error please inform admin'}), 500


@payments_bp.route('/user/balances', methods=['GET', 'POST'])
@token_required
def balances(current_user: any) -> tuple:
    get_flashed_messages()
    if current_user and current_user.uid:
        try:
            return render_template('payments/balances.html', heading='Make Payment', current_user=current_user,
                                   meta_tags=Metatags().set_home(), menu_open=True), 200

        except TemplateAssertionError as e:
            return render_template('error.html', heading='Error loading Page', message=e.message,
                                   meta_tags=Metatags().set_home()), 500
        except TemplateRuntimeError as e:
            return render_template('error.html', heading='Error loading Page', message=e.message,
                                   meta_tags=Metatags().set_home()), 500

    else:
        return render_template('error.html', heading='You are not authorized',
                               message="You are not authorized to view this page",
                               meta_tags=Metatags().set_home()), 401


@payments_bp.route('/user/transaction-history', methods=['GET', 'POST'])
@token_required
def transaction_history(current_user: any) -> tuple:
    get_flashed_messages()
    if current_user and current_user.uid:
        try:
            return render_template('payments/transactions.html', heading='Make Payment', current_user=current_user,
                                   meta_tags=Metatags().set_home(), menu_open=True), 200
        except TemplateAssertionError as e:
            return render_template('error.html', heading='Error loading Page', message=e.message,
                                   meta_tags=Metatags().set_home()), 500
        except TemplateRuntimeError as e:
            return render_template('error.html', heading='Error loading Page', message=e.message,
                                   meta_tags=Metatags().set_home()), 500
    else:
        return render_template('error.html', heading='You are not authorized',
                               message="You are not authorized to view this page",
                               meta_tags=Metatags().set_home()), 401


########################################################################################################################
# external endpoints
########################################################################################################################

@payments_bp.route('/auth/verify-eft-transaction/<path:path>', methods=['POST'])
@verify_external_auth_token
def verify_eft_payment(identity: str, path: str) -> tuple:
    """
        If this endpoint is executed it means that the EFT payment is verified
        :param identity:
        :param path:
        :return:
    """
    transaction_id: str = path
    try:
        transaction_instance = TransactionModel.query.filter_by(_transaction_id=transaction_id).first()
    except OperationalError as e:
        return render_template('error.html', heading='Database Error', message='error connecting to database',
                               meta_tags=Metatags().set_home()), 500
    # this function needs to be properly tested
    transaction_instance.verify()

    return jsonify({'message': 'payment successfully verified'}), 200
