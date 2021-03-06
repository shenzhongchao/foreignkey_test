# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-19 06:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('college_name', models.CharField(max_length=30)),
                ('location', models.CharField(max_length=30)),
                ('rank', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='College_major_score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('college_name', models.CharField(max_length=30)),
                ('major_name', models.CharField(max_length=30)),
                ('score', models.FloatField()),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.College')),
            ],
        ),
        migrations.CreateModel(
            name='Major',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('major_name', models.CharField(max_length=30)),
                ('major_code', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='college_major_score',
            name='major',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Major'),
        ),
    ]
