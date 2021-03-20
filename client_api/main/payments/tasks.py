"""
    Using transactions model read all unprocessed transactions
    then process them ,

    depending on the endpoint verification could be sent right away
    or will be sent later

    Payment Transactions that will be processed here include
        1. paypal transactions (in-case payment is scheduled) (or invoked right away)
        2. eft transaction (for other payment processing such as pay-fast)
        3. crypto-currency transactions

    TODO- learn how i can execute cron jobs in
        1. google app engine
        2. native python environments
"""

from .models import TransactionModel, PaymentModel


