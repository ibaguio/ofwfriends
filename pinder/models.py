import logging
from datetime import datetime, date

from django.db import models
from django.db.models import Q
from open_facebook import OpenFacebook

from pinder.here_api import haversine

def has_changed(instance, field):
    """Return true if field of instance has changed"""
    if not instance.pk:
        return False
    old_value = instance.__class__._default_manager.filter(pk=instance.pk).values(field).get()[field]
    return not getattr(instance, field) == old_value


class User(models.Model):
    MALE = 'M'
    FEMALE = 'F'

    GENDER = ((MALE, "Male"),
              (FEMALE, "Female"))

    fb_id = models.CharField(max_length=64)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    birthday = models.DateField()
    hometown = models.CharField(max_length=32, default='')
    job = models.CharField(max_length=32, default='')
    token = models.CharField(max_length=255)  # FB access token
    current_location = models.CharField(max_length=128, default="") # long lat
    location = models.CharField(max_length=65, default="")
    gender = models.CharField(max_length=1, choices=GENDER)

    def __str__(self):
        return "%s, %s" % (self.last_name, self.first_name)

    def distance_within(self, dist, dict_=True):
        """Return user's within *dist* kms."""
        q = (Q(_1=self) | Q(_2=self)) & Q(distance__lte=dist)
        data = UserDistance.objects.filter(q)
        d_ = []

        if dict_:
            for user in data:
                d_.append(dict(user))
        return data

    def distance_with(self, user):
        """Return distance of user with self"""
        assert self.pk != user.pk

        try:
            q = Q(_1=self, _2=user) | Q(_1=user, _2=self)
            return UserDistance.objects.get(q).distance

        except UserDistance.DoesNotExist:
            return None

    @property
    def picture_url(self):
        return "https://graph.facebook.com/%s/picture?type=square" % self.fb_id

    @property
    def coordinates(self):
        try:
            long_, lat_ = self.current_location.split(",")
            return (float(long_), float(lat_))
        except:
            return None

    @property
    def age(self):
        today = date.today()
        born = self.birthday
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    @classmethod
    def create(cls, fb_data, token=""):
        user = User(fb_id=fb_data['id'],
                    first_name=fb_data['first_name'],
                    last_name=fb_data['last_name'],
                    token=token,
                    birthday=datetime.strptime(fb_data['birthday'],
                                               "%m/%d/%Y"))
        if "hometown" in fb_data:
            user.hometown = fb_data['hometown']
        if "work" in fb_data:
            user.job = fb_data['work']
        if "location" in fb_data:
            user.location = fb_data['location']

        if "current_location" in fb_data:
            user.current_location = fb_data['current_location']

        user.save()
        if user.token:
            user.populate_likes()

        return user

    def save(self, *args, **kwargs):
        from pinder.tasks import task_generate_distance

        if not self.id or has_changed(self, "current_location"):
            # location has been updated
            # run tasks to calculate distance with other people
            # but first let us save to get the object id
            super(User, self).save(args, kwargs)
            # task_generate_distance.delay(self.pk)
            task_generate_distance(self.id)

        else:
            super(User, self).save(args, kwargs)

    def populate_likes(self):
        assert self.token

        try:
            fb = OpenFacebook(self.token)
            likes = fb.get("me/likes")['data']

            for like in likes:
                Interest.get_or_create(like, self)
        except Exception, e:
            logging.exception(e)

    @classmethod
    def create_dummy(cls):
        return cls.objects.create(first_name="Juan",
                                  last_name="Dela Cruz",
                                  birthday=date.today())

    def __iter__(self):
        for item in ["fb_id", "first_name", "last_name", "age",
                     "birthday", "hometown", "job", "location"]:
            if item == 'birthday':
                ret = (item, self.birthday.strftime("%m/%d/%y"))
            else:
                ret = (item, getattr(self, item))
            yield ret


class UserDistance(models.Model):
    """Store distance of each user with respect to every other user.

    Not a very optimal solution. But hey, this is a hackathon."""

    _1 = models.ForeignKey("User", related_name="distance_1")
    _2 = models.ForeignKey("User", related_name="distance_2")
    distance = models.IntegerField()  # in kms

    @classmethod
    def set_distance(cls, user_1, user_2):
        q = Q(_1=user_1, _2=user_2) | Q(_1=user_2, _2=user_1)

        # Get the UserDistance for this user
        try:
            ud = cls.objects.get(q)
        except UserDistance.DoesNotExist:
            ud = cls(_1=user_1, _2=user_2)

        if not user_1.coordinates or not user_2.coordinates:
            return

        long1, lat1 = user_1.coordinates
        long2, lat2 = user_2.coordinates
        distance = haversine(long1, lat1, long2, lat2)
        ud.distance = distance

        ud.save()
        return distance


class Interest(models.Model):
    fb_id = models.CharField(max_length=64, unique=True)
    user = models.ManyToManyField("User", related_name="interests")
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

    def __str__(self):
        return "[%s] %s" % (self.fb_id, self.interest)
