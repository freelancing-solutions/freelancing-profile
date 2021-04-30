from flask import  Blueprint, jsonify

from main import cache
from main.library.utils import const

notifications_bp = Blueprint('notifications', __name__, template_folder='../templates', static_folder='../static')


sample_notices: list = [
    {'notice': 'Welcome to Freelancing with AJ Ndou',
     'notice_time': '3 seconds ago',
     'notice_link': '/notifications/asdoaisdoasiud'
     },
    {'notice': 'How to create a freelance job',
     'notice_time': '3 seconds ago',
     'notice_link': 'notifications/asdakpsodkasodasd'
     }

]


# TODO- would be beneficial if i can find a way to include push notifications here
@notifications_bp.route('/notifications', methods=['GET', 'POST'])
@cache.cached(timeout=const.cache_timeout_hour)
def notifications() -> tuple:
    return jsonify({'status': 'success', 'notifications_list': sample_notices}), 200

# TODO try finalizing Notifications Delivery development