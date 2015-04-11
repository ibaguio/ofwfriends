import json
import requests
from math import radians, cos, sin, asin, sqrt

from django.conf import settings


def here_geocde(searchtext):
    try:

        data = (settings.HERE_APP_ID, settings.HERE_APP_CODE, searchtext)
        url = ("http://geocoder.cit.api.here.com/6.2/geocode.json"
               "?app_id=%s&app_code=%s&searchtext=%s" % data)

        r = requests.get(url)
        # print "response", r.text

        data = json.loads(r.text)['Response']["View"][0]["Result"]

        if "MatchType" in data[0] and data[0]["MatchType"] == "pointAddress":
            return [{'label': data['Label'],
                     'counter': data['Country'],
                     'state': data['State'],
                     'label': data['Label'],
                     'label': data['Label'],
                     'coordinates': data['Location']['DisplayPosition'],
                     'location_id': data['Location']['LocationId']
                     }]

        else:
            d_ = []
            for result in data:
                d_.append({
                    'label': result['Location']['Address']['Label'],
                    'country': result['Location']['Address']['Country'],
                    'state': result['Location']['Address']['State'],
                    # 'label': result['Label'],
                    # 'label': result['Label'],
                    'coordinates': result['Location']['DisplayPosition'],
                    'location_id': result['Location']['LocationId']
                    })

            return d_
    except Exception, e:
        import logging
        logging.exception(e)
        return data


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km
