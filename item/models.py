import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser as DjangoAbstractUser

class Item(models.Model):
    dttm_created = models.DateTimeField(default=datetime.datetime.now)
    dttm_deleted = models.DateTimeField(null=True, blank=True)

    price = models.FloatField()
    name = models.CharField(max_length=16, default='', blank=True)
    details = models.CharField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return self.name


class User(DjangoAbstractUser):
    dttm_deleted = models.DateTimeField(null=True, blank=True)

    SEX_FEMALE = 'F'
    SEX_MALE = 'M'
    SEX_CHOICES = (
        (SEX_FEMALE, 'Female',),
        (SEX_MALE, 'Male',),
    )

    sex = models.CharField(max_length=1,  choices=SEX_CHOICES)
    bought_items = models.ManyToManyField(Item)
    # multiple items insert
    # count_items=ArrayField(models.IntegerField, blank=True)

