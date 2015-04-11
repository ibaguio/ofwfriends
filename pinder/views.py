import json
import logging
import requests
from urlparse import urlparse, parse_qs

from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

from open_facebook import OpenFacebook

from pinder.here_api import *
from pinder.models import *

logger = logging.getLogger("views")

def landing_page(request):
    return render(request, "landing-page.html")

def test_login(request):
    return render(request, "test-login.html")

def api_me(requests):
    fb_id = requests.GET.get("me")
    resp = {"status": "success"}

    try:
        me = User.objects.get(fb_id=fb_id)
        resp["data"] = dict(me)

    except Exception, e:
        resp["status"] = "fail"
        resp["error"] = e

    return HttpResponse(json.dumps(resp))

def api_register(requests):
    try:
        fb_id = requests.POST.get("me")
        token = requests.POST.get("token")


        user = User.get_user_from_id(fb_id, token)

        return HttpResponse(json.dumps({"status": "success"}))

    except Exception, e:
        err_msg = "e"
        return HttpResponse(json.dumps({"status": "fail",
                                        "message": err_msg}))

def api_search(requests):
    """Search for locations given a query."""
    query = requests.GET.get("query")

    return HttpResponse(json.dumps({"status": "success",
                                    "result": here_geocde(query)}))

def api_people_nearby(requests):
    fb_id = requests.GET.get("me")
    distance = int(requests.GET.get("distance"))

    me = User.objects.get(id=fb_id)
    data = me.distance_within(distance)

    return HttpResponse(json.dumps({"status": "success",
                                    "result": data}))

def fb_auth_handler(request):
    # Retrieve oAuth response
    response = urlparse(request.get_full_path())
    query = parse_qs(response.query)

    # Handle oAuth initial request error
    if "error" in query and "access_denied" in query["error"] and \
            "user_denied" in query["error_reason"]:
        try:
            logger.warning("Facebook returned error: %s" % query["error"])
        except KeyError:
            err_msg = "Please login and allow Facebook to continue."
            return HttpResponse(json.dumps({"status": "fail",
                                            "message": err_msg}))

    # Recreate the redirect_uri
    redir_path = request.get_full_path()

    logger.info("exchanging code for accesstoken...")

    redirect_uri = request.META['wsgi.url_scheme'] + "://" +\
                   request.get_host() + reverse("fb_auth_handler")

    payload = {
        "client_id": settings.FACEBOOK_APP_ID,
        "redirect_uri": redirect_uri,
        "client_secret": settings.FACEBOOK_APP_SECRET,
        "code": query["code"][0]
    }
    xrequest = requests.get("https://graph.facebook.com/oauth/access_token",
                            params=payload)

    # Handle oAuth secondary request error
    fbresponse = parse_qs(xrequest.text)

    if "error" in fbresponse or not len(fbresponse):
        # TODO: Error handling
        if "error" in fbresponse:
            err_msg = "FB returned error: %s" % fbresponse["error"]
            logger.warning(err_msg)

        else:
            err_msg = "User fb token expired."
            logger.warning(err_msg)

        return HttpResponse(json.dumps({"status": "fail",
                                        "message": err_msg}))

    # Acquire accesstoken
    accesstoken = fbresponse["access_token"][0]
    # Acquire userinfo
    graph = OpenFacebook(accesstoken)
    user_data = graph.get('me')

    user = User.create(user_data, token=accesstoken)

    if user:
        return HttpResponse(json.dumps({"status": "success",
                                        "data": dict(user)}))
    else:
        return HttpResponse(json.dumps({"status": "fail"}))
