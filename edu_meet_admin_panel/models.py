# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AcademicSubject(models.Model):
    name = models.CharField()
    description = models.CharField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'academic_subject'


class AlembicVersion(models.Model):
    version_num = models.CharField(primary_key=True, max_length=32)

    class Meta:
        managed = False
        db_table = 'alembic_version'


class Order(models.Model):
    student = models.ForeignKey('User', models.DO_NOTHING)
    tutor = models.ForeignKey('User', models.DO_NOTHING, related_name='order_tutor_set')
    slot = models.ForeignKey('Slot', models.DO_NOTHING)
    subject = models.ForeignKey(AcademicSubject, models.DO_NOTHING)
    status = models.TextField()  # This field type is a guess.
    comment = models.CharField(blank=True, null=True)
    date = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'order'


class Slot(models.Model):
    is_available = models.BooleanField()
    date = models.DateTimeField()
    time_start = models.TimeField()
    time_end = models.TimeField()
    tutor = models.ForeignKey('User', models.DO_NOTHING)
    student = models.ForeignKey('User', models.DO_NOTHING, related_name='slot_student_set', blank=True, null=True)
    comment = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'slot'


class User(models.Model):
    tg_id = models.BigIntegerField(unique=True)
    username = models.CharField(unique=True, blank=True, null=True)
    is_admin = models.BooleanField()
    timezone = models.CharField()
    created_at = models.DateTimeField()
    last_activity = models.DateTimeField()
    updated_at = models.DateTimeField()
    first_name = models.CharField(unique=True, blank=True, null=True)
    last_name = models.CharField(unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'
