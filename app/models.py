# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class College(models.Model):
    college_name=models.CharField(max_length=30)
    location=models.CharField(max_length=30)
    rank=models.IntegerField()

    def __unicode__(self):
        return self.college_name

class Major(models.Model):
    major_name=models.CharField(max_length=30)
    major_code = models.CharField(max_length=30)

    def __unicode__(self):
        return self.major_name

class College_major_score(models.Model):
    college=models.ForeignKey(College,null=True)
    college_name=models.CharField(max_length=30)
    major = models.ForeignKey(Major,null=True)
    major_name = models.CharField(max_length=30)
    score=models.FloatField()

    def __unicode__(self):
        return "%s %s %s" % (self.college_name,self.major_name,self.score)