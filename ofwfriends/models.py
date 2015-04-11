from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    birthday = models.DateField()
    province = models.CharField(max_length=32)
    job = models.CharField(max_length=32)


class Interest(models.Model):
    user = models.ForeignKey(User, related_name="interests")
    interest = models.CharField(max_length=32)
