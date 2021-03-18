from flask import render_template, request, Blueprint, get_flashed_messages
from ..library import Metatags, logged_user
from .models import PaymentModel, TransactionModel

payments_bp = Blueprint('payments', __name__)


@payments_bp.route('/user-payments', methods=['GET', 'POST'])
@logged_user
def payments(current_user) -> str:
    return render_template('payments.html', heading='Payments', current_user=current_user,
                           meta_tags=Metatags().set_home(), menu_open=True)
