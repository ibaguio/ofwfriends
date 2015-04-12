from django.conf import settings


def static_vars(request):
    return {
        'fb_app_id': settings.FACEBOOK_APP_ID,
        'fb_scope': ('user_birthday,user_likes,user_hometown,'
                     'user_work_history,user_location'),
        'fb_auth_redirect': settings.FB_AUTH_REDIRECT,
        'HERE_APP_ID': settings.HERE_APP_ID,
        'HERE_APP_CODE': settings.HERE_APP_CODE,
        'STATIC_UR:': '',
    }
