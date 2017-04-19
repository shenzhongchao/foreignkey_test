# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from app.models import College, Major, College_major_score
from django.contrib import admin

# Register your models here.

admin.site.register(Major)
admin.site.register(College)
admin.site.register(College_major_score)