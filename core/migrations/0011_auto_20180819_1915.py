# Generated by Django 2.1 on 2018-08-19 19:15

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_movie_ratings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='ratings',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
