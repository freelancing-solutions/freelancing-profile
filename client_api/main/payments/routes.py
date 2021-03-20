from flask import render_template, request, Blueprint, get_flashed_messages, jsonify
from ..library import Metatags, logged_user, token_required, verify_external_auth_token
from ..library.utils import const, timestamp
from .models import PaymentModel, TransactionModel
from jinja2 import TemplateAssertionError, TemplateRuntimeError
from main import db

payments_bp = Blueprint('payments', __name__, template_folder='../templates', static_folder='../static')


@payments_bp.route('/user/payments', methods=['GET', 'POST'])
@token_required
def payments(current_user) -> str:
    get_flashed_messages()
    if current_user and current_user.uid:
        if request.method == "GET":
            payments_instance = PaymentModel.query.filter_by(_uid=current_user.uid).all()
            # TODO- learn how to access transactions from
            try:
                return render_template('payments.html', heading='Payments', payments=payments_instance,
                                       transactions_list=payments_instance.transactions,
                                       current_user=current_user, meta_tags=Metatags().set_home(), menu_open=True)

            except TemplateAssertionError as e:
                return render_template('error.html', heading='Error loading Page', message=e.message,
                                       meta_tags=Metatags().set_home())
            except TemplateRuntimeError as e:
                return render_template('error.html', heading='Error loading Page', message=e.message,
                                       meta_tags=Metatags().set_home())
        else:
            # TODO- need to decide what to do here
            pass

    else:
        message = ''' 
            You are not authorized to view payment information, 
            <a href="{{ url_for('users.login')}}">please consider login in</a>
        '''
        return render_template('error.html', heading='Not Authorized', message=message, meta_tags=Metatags().set_home())


@payments_bp.route('/user/make-payment/<path:path>', methods=['GET', 'POST'])
@token_required
def make_payment(current_user, path) -> any:
    get_flashed_messages()
    if current_user and current_user.uid:
        if request.method == "GET":
            payment_id = path
            try:
                payment_instance = PaymentModel.query.filter_by(_payment_id=payment_id).first()
            except Exception as e:
                message = '''
                    Sorry we are unable to locate the payment record referenced
                    however try making payments directly from freelance jobs page
                '''
                return render_template('error.html', heading='Payment Record Not found', message=message,
                                       meta_tags=Metatags().set_home())
            try:
                return render_template('payments/payment.html', heading='Make Payment', current_user=current_user,
                                       meta_tags=Metatags().set_home(), menu_open=True,
                                       payment_id=payment_instance.payment_id)

            except TemplateAssertionError as e:
                return render_template('error.html', heading='Error loading Page', message=e.message,
                                       meta_tags=Metatags().set_home())
            except TemplateRuntimeError as e:
                return render_template('error.html', heading='Error loading Page', message=e.message,
                                       meta_tags=Metatags().set_home())
        else:
            # NOTE: this is where the user is creating the actual transaction
            try:
                payment_details = request.get_json()
            except Exception as e:
                message = '''
                    Error reading your submitted payment information consider enabling javascript on your browser                                         
                '''
                return render_template('error.html', heading='Unable to read payment information', message=message,
                                       meta_tags=Metatags().set_home())

            if 'method' not in payment_details:
                return jsonify({'message': 'Please select payment method'}), 500
            if 'amount' not in payment_details:
                return jsonify({'message': 'Payment amount not filled in correctly'}), 500
            if 'currency' not in payment_details:
                return jsonify({'message': 'Please select your currency of payment'}), 500
            if 'payment_id' not in payment_details:
                return jsonify({'message': 'Snap something went horribly wrong please reload your page'}), 500

            amount = payment_details['amount']
            currency = payment_details['currency']
            payment_id = payment_details['payment_id']
            method = payment_details['method']

            payment_instance = PaymentModel.query.filter_by(_payment_id=payment_id).first()
            if payment_instance and (payment_instance.amount > int(amount)) and (currency == payment_instance.currency):
                new_transaction = TransactionModel(payment_id=payment_id, method=method, amount=amount,
                                                   currency=currency)

                # TODO- first try verifying payment information before you can actually substract payment amount
                # payment_instance.amount -= int(amount)
                payment_instance.last_transaction_date = timestamp()
                db.session.update(payment_instance)
                db.session.add(new_transaction)
                db.session.commit()
                
                return jsonify({'message': 'Successfully created new transaction'}), 200
            else:
                message = '''
                    This is awkward , something went horribly wrong on our end 
                    <a href="{{ url_for('main.contact')}}">please consider reporting this error to our admin</a> 
                '''
                return render_template('error.html', heading='Unable to read payment information', message=message,
                                       meta_tags=Metatags().set_home())


@payments_bp.route('/user/balances', methods=['GET', 'POST'])
@token_required
def balances(current_user) -> str:
    get_flashed_messages()
    try:
        return render_template('payments/balances.html', heading='Make Payment', current_user=current_user,
                               meta_tags=Metatags().set_home(), menu_open=True)

    except TemplateAssertionError as e:
        return render_template('error.html', heading='Error loading Page', message=e.message,
                               meta_tags=Metatags().set_home())
    except TemplateRuntimeError as e:
        return render_template('error.html', heading='Error loading Page', message=e.message,
                               meta_tags=Metatags().set_home())


@payments_bp.route('/user/transaction-history', methods=['GET', 'POST'])
@token_required
def transaction_history(current_user) -> str:
    get_flashed_messages()
    try:
        return render_template('payments/transactions.html', heading='Make Payment', current_user=current_user,
                               meta_tags=Metatags().set_home(), menu_open=True)
    except TemplateAssertionError as e:
        return render_template('error.html', heading='Error loading Page', message=e.message,
                               meta_tags=Metatags().set_home())
    except TemplateRuntimeError as e:
        return render_template('error.html', heading='Error loading Page', message=e.message,
                               meta_tags=Metatags().set_home())


########################################################################################################################
# external endpoints
########################################################################################################################

@payments_bp.route('/auth/verify-eft-transaction/<path:path>', methods=['POST'])
@verify_external_auth_token
def verify_eft_payment(identity, path):
    """
        If this endpoint is executed it means that the EFT payment is verified
        :param identity:
        :param path:
        :return:
    """
    transaction_id = path
    transaction_instance = TransactionModel.query.filter_by(_transaction_id=transaction_id).first()
    transaction_instance.verify()

    return jsonify({'message': 'payment successfully verified'}), 200







