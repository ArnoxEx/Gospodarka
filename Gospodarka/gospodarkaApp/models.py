# -*- coding: utf-8 -*-

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from datetime import datetime
import re

class Address(models.Model):
    id = models.AutoField(primary_key=True)
    err_msg = "Nazwy miast moga skladac sie wylacznie z liter i nie moga byc krotsze niz dwie litery".encode("utf-8")
    name_regex = re.compile(r'^[A-ZŁĄŻŹĆĘŃÓĘ][\x20a-złążźćęńóęA-ZŁĄŻŹĆĘŃÓĘ]+$', re.UNICODE)
    name_validator = RegexValidator(regex=name_regex, message=err_msg)
    city = models.CharField(max_length=64, validators=[name_validator])
    street = models.CharField(max_length=64)
    numb = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=20)

    def full_address(self):
        return 'ul. ' + street + numb + ', ' + city + postal_code

    class Meta:
        managed = False
        db_table = 'address'


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    place = models.ForeignKey('Object', models.DO_NOTHING, db_column='place')
    max_tickets = models.PositiveIntegerField()
    time = models.DateField(default=datetime.now)
    ticket_price = models.PositiveIntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'event'


class Object(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.ForeignKey(Address, models.DO_NOTHING, db_column='address')
    name = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'object'


class Ordr(models.Model):
    id = models.AutoField(primary_key=True)
    usr = models.ForeignKey('Usr', models.DO_NOTHING, db_column='usr')
    event = models.ForeignKey(Event, models.DO_NOTHING, db_column='event')
    status = models.ForeignKey('Status', models.DO_NOTHING, db_column='status')
    numb = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'ordr'


class Status(models.Model):
    id = models.AutoField(primary_key=True)
    value = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'status'


class Usr(models.Model):
    user = models.OneToOneField(User)

    id = models.AutoField(primary_key=True)
    address = models.ForeignKey(Address, models.DO_NOTHING, db_column='address')
    phone_regex = RegexValidator(regex=r'^\+48\d{9}$',
        message="Numer telefonu musi byc formatu: +48xxxxxxxxx.")
    phone = models.CharField(validators=[phone_regex], blank=True, null=True, default='+48',
        max_length=12)
    # activation_key = models.CharField(max_length=40, blank=True)
    # key_expires = models.DateTimeField(default=datetime.now)

    class Meta:
        managed = False
        db_table = 'usr'


class Usrobject(models.Model):
    id = models.AutoField(primary_key=True)
    usr = models.ForeignKey(Usr, models.DO_NOTHING, db_column='usr')
    object = models.ForeignKey(Object, models.DO_NOTHING, db_column='object')

    class Meta:
        managed = False
        db_table = 'usrobject'

