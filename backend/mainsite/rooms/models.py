# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class NormalRoom(models.Model):
    room_no = models.CharField(unique=True, max_length=255)
    availability = models.IntegerField(default=1)
    student = models.CharField(default='', max_length=255)
    dept = models.CharField(default='', max_length=255)
    _id = models.CharField(default='', max_length=255)
    mobile_num = models.IntegerField(default=0)
    guest_name = models.CharField(default='', max_length=255)
    guest_num = models.IntegerField(default=0)
    check_in = models.CharField(default='', max_length=255)
    check_out = models.CharField(default='', max_length=255)
    relation = models.CharField(default='', max_length=255)
    purpose = models.CharField(default='', max_length=255)
    food = models.IntegerField(default=0)
    dt_created = models.DateTimeField(auto_now_add=True)

