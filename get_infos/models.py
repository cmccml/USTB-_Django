# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Problems(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    title = models.CharField(max_length=255)
    submitted = models.IntegerField(blank=True, null=True)
    accepted = models.IntegerField(blank=True, null=True)
    ac_ratio = models.FloatField(blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    difficulty = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'problems'


class ProblemsRepresentatives(models.Model):
    problem = models.ForeignKey(Problems, models.DO_NOTHING, blank=True, null=True)
    representative = models.ForeignKey('RepresentativeTags', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'problems_representatives'


class RepresentativeTags(models.Model):
    id = models.OneToOneField('Tags', models.DO_NOTHING, db_column='id', primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    isa = models.ForeignKey('self', models.DO_NOTHING, db_column='isa', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'representative_tags'


class Solutions(models.Model):
    problem = models.ForeignKey(Problems, models.DO_NOTHING)
    title = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    visit = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'solutions'


class Tags(models.Model):
    name = models.CharField(max_length=255)
    representative = models.ForeignKey('self', models.DO_NOTHING, db_column='representative', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tags'
