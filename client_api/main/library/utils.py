import os, random, string, time

char_set = string.ascii_lowercase + string.digits


def is_development() -> bool:
    return True if os.environ['SERVER_SOFTWARE'].lower().startswith('development') else False


class Const:
    uuid_len: int = 36
    username_len: int = 128
    email_len: int = 128
    cell_len: int = 13
    link_len: int = 256
    password_len: int = 256
    names_len: int = 256
    id_len: int = 64
    cell_token_len: int = 8
    project_name_len: int = 512
    project_cat_len: int = 256
    description_len: int = 32768
    project_status_len: int = 12
    default_project_hours: int = 7 * 24  # 7 days by 24 hours
    currency_len: int = 6
    subject_len: int = 256
    body_len: int = 32768
    reason_len: int = 256
    response_len: int = 32768
    transaction_method_len: int = 16
    currency_list: list = ['usd', 'USD', "r", 'R']
    payment_methods: list = ['eft', 'paypal', 'direct-deposit', 'crypto-currency']

    title_len: int = 256
    article_len: int = 65536
    draft_len: int = 128

    ip_length: int = 16
    cache_timeout_hour: int = 1 if is_development() else 60 * 60


const = Const()


def create_id(size: int = 64, chars: str = char_set) -> str: return ''.join(random.choice(chars) for x in range(size))


def timestamp() -> int: return int(float(time.time()))


def timestamp_difference(stamp1, stamp2) -> int: return int(stamp1 - stamp2)


def is_email(email) -> bool:
    # TODO- verify email here with regular expressions
    return True


def is_cell(cell) -> bool:
    # TODO- verify cell number here
    return True


def replace_html(s) -> str:
    """
        given an html string remove all html tags and leave only string
    :param s:
    :return: string
    """

    # TODO- optimize this algorithm and test for correctness
    def _replace_tag(in_s, in_marks) -> str:
        print("replacing", in_s)
        return "{} {}".format(in_s.split[:in_marks[0]][0], in_s.split[:in_marks[0]][1][:in_marks[1]])

    marks: list = [0, 0]
    for c, i in enumerate(s):
        if c == "<":
            marks[0] = i
        if c == ">":
            marks[1] = i
        if marks[1] != 0:
            s = _replace_tag(s, marks)
            marks[0] = 0
            marks[1] = 0
    return s
