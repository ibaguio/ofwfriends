from datetime import datetime, date

from django.db import models
from open_facebook import OpenFacebook


class User(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    birthday = models.DateField()
    hometown = models.CharField(max_length=32, default='')
    job = models.CharField(max_length=32, default='')
    token = models.CharField(max_length=255)  # FB access token

    @classmethod
    def create(cls, fb_data, token=""):
        user = User(first_name=fb_data['first_name'],
                    last_name=fb_data['last_name'],
                    token=token,
                    birthday=datetime.strptime(fb_data['birthday'],
                                               "%m/%d/%Y"))
        if "hometown" in fb_data:
            user.hometown = fb_data['hometown']
        if "work" in fb_data:
            user.job = fb_data['work']

        user.save()
        user.populate_likes()

        return user

    def populate_likes(self):
        assert self.token

        try:
            fb = OpenFacebook(self.token)
            likes = fb.get("me/likes")['data']

            for like in likes:
                Interest.get_or_create(like, self)
        except Exception, e:
            import logging
            logging.exception(e)

    @classmethod
    def create_dummy(cls):
        return cls.objects.create(first_name="Juan",
                                  last_name="Dela Cruz",
                                  birthday=date.today())


class Interest(models.Model):
    fb_id = models.CharField(max_length=64, unique=True)
    user = models.ManyToManyField(User, related_name="interests")
    interest = models.CharField(max_length=32)

    @classmethod
    def get_or_create(cls, item, user=None):
        try:
            like = Interest.objects.get(fb_id=item['id'])

        except Interest.DoesNotExist:
            like = Interest(fb_id=item['id'], interest=item['name'])
            like.save()

        if user:
            like.user.add(user)

        return like
