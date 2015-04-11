import random
from datetime import date

from pinder.models import User

JOBS = ["Seaman", "Nurse", "Domestic Worker", "Digital Nomad", "Engineer"]


def create_test_users():
    users = [{
        'id': '123',
        'first_name': 'Juan',
        'last_name': 'Dela Cruz',
        'birthday': "01/10/1990",
        'hometown': 'Cebu',
        'job': random.choice(JOBS),
        'current_location': '51.50643,-0.12721',  # london city
        'gender': 'F',
    }, {
        'id': '124',
        'first_name': 'Arnel',
        'last_name': 'Angeles',
        'birthday': "01/10/1980",
        'hometown': 'Davao',
        'job': random.choice(JOBS),
        'current_location': '51.5043983,-0.18858',  # kensington palace
        'gender': 'M'
    }, {
        'id': '125',
        'first_name': 'Dionisia',
        'last_name': 'Santos',
        'birthday': "1/10/1985",
        'hometown': 'Quezon City',
        'job': random.choice(JOBS),
        'current_location': '51.4909897,-0.14952',  #buckingham palace
        'gender': 'M'
    }]

    for u in users:
        User.create(u)
# {
#         'id': '',
#         'first_name': 'Arnel',
#         'last_name': '',
#         'birthday': date(1980, 1, 10),
#         'hometown': '',
#         'job': random.choice(JOBS),
#         'current_location': 'long_,lat_',
#         'gender': 'M'
#     }
