import requests
import hashlib
import re
from datetime import datetime

from pinder.settings import CHIKKA_ID, CHIKKA_KEY, CHIKKA_SHORT_CODE


def send_sms(number, message):
    """Send SMS using Chikka API"""

    def get_msg_id():
        md5 = hashlib.md5()
        md5.update(number + datetime.strftime(datetime.now(), "%d/%m/%y %H:%M"))
        return md5.hexdigest()

    try:
        # number must start with 639
        number = re.sub(r'^09', '639', number)
        assert len(number) == 12

        # msg len must not exceed 420
        # see chikka docs: https://api.chikka.com/docs/handling-messages#send-sms
        assert len(message) < 421

        data = {
            'message_type': 'SEND',
            'client_id': CHIKKA_ID,
            'secret_key': CHIKKA_KEY,
            'shortcode': CHIKKA_SHORT_CODE,
            'mobile_number': number,
            'message': message,
            'message_id': get_msg_id()
        }

        return requests.post('https://post.chikka.com/smsapi/request', data)
    except Exception, e:
        print e
