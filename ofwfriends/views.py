import logging
from urlparse import urlparse, parse_qs

from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect

from open_facebook import OpenFacebook


from ofwfriends.models import *

logger = logging.getLogger(__name__)

def landing_page(request):
    return render("landing-page.html")

def fb_auth_handler(request):
    # Retrieve oAuth response
    response = urlparse(request.get_full_path())
    query = parse_qs(response.query)

    # Handle oAuth initial request error
    if "error" in query and "access_denied" in query["error"] and \
            "user_denied" in query["error_reason"]:
        try:
            authSession.warning("Facebook returned error: %s" % query["error"])
            return redirect(authSession.captive_url)
        except KeyError:
            return HttpResponse("Please login and allow Facebook to continue.")

    # Recreate the redirect_uri
    redir_path = request.get_full_path()

    logger.info("exchanging code for accesstoken...")
    payload = {
        "client_id": settings.FACEBOOK_APP_ID,
        "redirect_uri": fb_auth_redirect,
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
            authSession.warning("FB returned error: %s" % fbresponse["error"])
        else:
            authSession.warning("User fb token expired.")

        return redirect_to_captive_url(request, authSession)

    # Acquire accesstoken
    accesstoken = fbresponse["access_token"][0]

    # Acquire userinfo
    graph = OpenFacebook(accesstoken)
    user_data = graph.get('me')
