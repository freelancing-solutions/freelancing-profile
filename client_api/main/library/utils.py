import os, random, string, time


class Const:
    uuid_len = 36
    username_len = 128
    email_len = 128
    cell_len = 13
    link_len = 256
    password_len = 256
    names_len = 256
    id_len = 64
    project_name_len = 512
    project_cat_len = 256
    description_len = 32768
    project_status_len = 12
    default_project_hours = 7 * 24  # 7 days by 24 hours
    currency_len = 6
    subject_len = 256
    body_len = 32768
    reason_len = 256
    response_len = 32768
    transaction_method_len = 16
    currency_list = ['$', 'R', 'r']
    payment_methods = ['eft', 'paypal', 'direct-deposit', 'crypto-currency']

    title_len = 256
    article_len = 65536
    draft_len = 128


const = Const()


def create_id(size=const.id_len, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def timestamp():
    return int(float(time.time()) * 1000)


def timestamp_difference(stamp1, stamp2):
    return int(stamp1 - stamp2)


def is_development():
    if os.environ['SERVER_SOFTWARE'].lower().startswith('development'):
        return True
    return False
