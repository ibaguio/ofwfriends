import random
import json
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

def create_many_users():
    JSON_TEXT = """[{"first_name": "Nia", "last_name": "Colinayo", "location": "Quezon City, Philippines", "gender": "F", "job": "Nurse", "hometown": "Tacloban City", "id": "100007239634330", "birthday": "08/19/1995"}, {"first_name": "Theodore Joseph", "last_name": "Jumamil", "location": "Quezon City, Philippines", "gender": "M", "job": "Domestic Worker", "hometown": "Quezon City, Philippines", "id": "100007055736414", "birthday": "03/22/1989"}, {"first_name": "Kix", "last_name": "Panganiban", "location": "Quezon City, Philippines", "gender": "M", "job": "Nurse", "hometown": "Candaba, Pampanga", "id": "1639744092", "birthday": "09/05/1994"}, {"first_name": "Lorenzo", "last_name": "Valentino", "location": "Antipolo, Rizal", "gender": "M", "job": "Engineer", "hometown": "Quezon City, Philippines", "id": "545692783", "birthday": "04/10/1991"}, {"first_name": "Shawn", "last_name": "Calda", "location": "Muntinlupa City", "gender": "M", "job": "Seaman", "hometown": "Muntinlupa City", "id": "100000266041692", "birthday": "12/25/1991"}, {"first_name": "Thor", "last_name": "Manlangit", "location": "Quezon City, Philippines", "gender": "M", "job": "Digital Nomad", "hometown": "Mangagoy, Surigao Del Sur, Philippines", "id": "1296199129", "birthday": "08/06/1989"}, {"first_name": "Jeffrey", "last_name": "Burce", "location": "Quezon City, Philippines", "gender": "M", "job": "Domestic Worker", "hometown": "Quezon City, Philippines", "id": "100003871743637", "birthday": "01/08/1991"}, {"first_name": "Karl", "last_name": "Legazpi", "location": "Diliman, Quezon City, Philippines", "gender": "M", "job": "Engineer", "hometown": "Puerto Princesa", "id": "1673144713", "birthday": "10/31/1995"}, {"first_name": "Roxette", "last_name": "Manimbo", "location": "Quezon City, Philippines", "gender": "F", "job": "Digital Nomad", "hometown": "Quezon City, Philippines", "id": "100007294531488", "birthday": "05/31/1994"}, {"first_name": "Julia", "last_name": "Barrameda", "location": "Quezon City, Philippines", "gender": "F", "job": "Nurse", "hometown": "Cagayan de Oro, Philippines", "id": "1356376845", "birthday": "09/25/1994"}, {"first_name": "Ryan", "last_name": "Ruedas", "location": "Imus, Cavite", "gender": "M", "job": "Seaman", "hometown": "Caloocan", "id": "778207199", "birthday": "07/12/1988"}, {"first_name": "Gladdys", "last_name": "Talip", "location": "Quezon City, Philippines", "gender": "F", "job": "Seaman", "hometown": "Tambulig, Zamboanga del Sur", "id": "1018830593", "birthday": "09/19/1986"}, {"first_name": "Darwin", "last_name": "Yabes", "location": "Quezon City, Philippines", "gender": "M", "job": "Engineer", "hometown": "Manila, Philippines", "id": "100001485227170", "birthday": "08/06/1986"}, {"first_name": "Meatyboy", "last_name": "Heckler", "location": "Quezon City, Philippines", "gender": "M", "job": "Digital Nomad", "hometown": "Bacolor, Pampanga", "id": "100006980075654", "birthday": "03/23/1971"}, {"first_name": "Lorrie", "last_name": "Corpuz", "location": "Mangatarem, Pangasinan", "gender": "F", "job": "Seaman", "hometown": "Mangatarem, Pangasinan", "id": "100004341935273", "birthday": "03/09/1986"}, {"first_name": "Marianne", "last_name": "Del Rey", "location": "Miagao, Iloilo, Philippines", "gender": "F", "job": "Nurse", "hometown": "Kalibo, Aklan", "id": "1674969405", "birthday": "05/02/1994"}, {"first_name": "Yui", "last_name": "Firme", "location": "Quezon City, Philippines", "gender": "F", "job": "Digital Nomad", "hometown": "Naga City", "id": "664148498", "birthday": "10/08/1986"}, {"first_name": "Aiza", "last_name": "Lovedorial", "location": "Tayabas, Quezon", "gender": "F", "job": "Digital Nomad", "hometown": "Quezon City, Philippines", "id": "100001598299957", "birthday": "07/17/1989"}, {"first_name": "Jia", "last_name": "Fuentes", "location": "Pasig", "gender": "F", "job": "Domestic Worker", "hometown": "Pasig", "id": "646066080", "birthday": "02/17/1990"}, {"first_name": "Ross", "last_name": "Calzadora", "location": "Cubao, Quezon City, Philippines", "gender": "F", "job": "Digital Nomad", "hometown": "Quezon City, Philippines", "id": "100000403235281", "birthday": "10/09/1993"}, {"first_name": "Riciela", "last_name": "Tuazon", "location": "Quezon City, Philippines", "gender": "F", "job": "Seaman", "hometown": "Quezon City, Philippines", "id": "100002642732737", "birthday": "12/13/1985"}, {"first_name": "Joon", "last_name": "Crsna", "location": "Quezon City, Philippines", "gender": "F", "job": "Digital Nomad", "hometown": "Quezon City, Philippines", "id": "100002564084205", "birthday": "06/30/1994"}, {"first_name": "Samantha Mae", "last_name": "Namuhe", "location": "Quezon City, Philippines", "gender": "F", "job": "Engineer", "hometown": "Lagawe, Ifugao", "id": "100002695000483", "birthday": "08/27/1994"}, {"first_name": "Mona Liza", "last_name": "Bacurio", "location": "Quezon City, Philippines", "gender": "F", "job": "Seaman", "hometown": "Meycauayan, Bulacan", "id": "600655496", "birthday": "09/23/1986"}, {"first_name": "Maf", "last_name": "Cipriano", "location": "Quezon City, Philippines", "gender": "F", "job": "Digital Nomad", "hometown": "Pagadian City", "id": "100002284770264", "birthday": "07/18/1991"}, {"first_name": "Franz", "last_name": "Libre", "location": "Quezon City, Philippines", "gender": "M", "job": "Seaman", "hometown": "South Digos, Davao Del Sur, Philippines", "id": "1099077788", "birthday": "03/14/1994"}, {"first_name": "Layza", "last_name": "Nepomuceno", "location": "Antipolo, Rizal", "gender": "F", "job": "Digital Nomad", "hometown": "Quezon City, Philippines", "id": "1717044693", "birthday": "08/03/1993"}, {"first_name": "Mariella", "last_name": "Gotladera", "location": "Quezon City, Philippines", "gender": "F", "job": "Nurse", "hometown": "Quezon City, Philippines", "id": "1636121217", "birthday": "08/18/1993"}, {"first_name": "Joey", "last_name": "Furio", "location": "Quezon City, Philippines", "gender": "M", "job": "Seaman", "hometown": "Quezon City, Philippines", "id": "1224754181", "birthday": "01/10/1994"}, {"first_name": "Daianne", "last_name": "Zipagan", "location": "Imus, Cavite", "gender": "F", "job": "Nurse", "hometown": "Seoul, Korea", "id": "100003085208894", "birthday": "06/22/1992"}, {"first_name": "Alyson", "last_name": "Yap", "location": "Quezon City, Philippines", "gender": "M", "job": "Engineer", "hometown": "Quezon City, Philippines", "id": "814144851", "birthday": "04/01/1981"}, {"first_name": "Jelou", "last_name": "Tiston", "location": "Quezon City, Philippines", "gender": "F", "job": "Engineer", "hometown": "San Miguel, Bulacan", "id": "1178384460", "birthday": "08/06/1994"}, {"first_name": "Xtian", "last_name": "Ordinario", "location": "Quezon City, Philippines", "gender": "M", "job": "Engineer", "hometown": "Daet, Camarines Norte", "id": "100000202386846", "birthday": "02/17/1978"}, {"first_name": "Gab", "last_name": "Tabilin", "location": "Quezon City, Philippines", "gender": "M", "job": "Engineer", "hometown": "Quezon City, Philippines", "id": "554076683", "birthday": "09/30/1993"}, {"first_name": "Arcey", "last_name": "Yu", "location": "Manila, Philippines", "gender": "M", "job": "Seaman", "hometown": "Manila, Philippines", "id": "1105112863", "birthday": "11/13/1988"}, {"first_name": "Olin", "last_name": "Ysmael", "location": "Quezon City, Philippines", "gender": "F", "job": "Digital Nomad", "hometown": "Quezon City, Philippines", "id": "560749246", "birthday": "08/20/1989"}, {"first_name": "BJ", "last_name": "David", "location": "Taguig", "gender": "M", "job": "Engineer", "hometown": "Quezon City, Philippines", "id": "1015040902", "birthday": "08/17/1982"}, {"first_name": "Emmanuel", "last_name": "Aguila", "location": "Quezon City, Philippines", "gender": "M", "job": "Digital Nomad", "hometown": "Quezon City, Philippines", "id": "599312941", "birthday": "05/20/1983"}, {"first_name": "Jhon", "last_name": "Manuncia", "location": "Quezon City, Philippines", "gender": "M", "job": "Digital Nomad", "hometown": "Quezon City, Philippines", "id": "1557042051", "birthday": "02/01/1989"}, {"first_name": "Lianne", "last_name": "Dela Cruz", "location": "Pasig", "gender": "F", "job": "Digital Nomad", "hometown": "Pasig", "id": "100000147228241", "birthday": "03/27/1995"}, {"first_name": "Renz", "last_name": "Correo", "location": "Antipolo, Rizal", "gender": "M", "job": "Digital Nomad", "hometown": "Antipolo, Rizal", "id": "1458702735", "birthday": "07/18/1994"}, {"first_name": "Koy", "last_name": "Garcia", "location": "Quezon City, Philippines", "gender": "M", "job": "Engineer", "hometown": "Tacloban City", "id": "1595209489", "birthday": "11/21/1990"}]"""
    count = 0
    users = json.loads(JSON_TEXT)
    for u in users:
        try:
            u['location'] = {
                'name': u['location']
            }
            User.create(u)
            count += 1
        except Exception, e:
            import logging
            logging.exception(e)
            raise e

    print "created", count, "users"
