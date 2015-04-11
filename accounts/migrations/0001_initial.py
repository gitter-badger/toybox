# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('signature', models.CharField(max_length=1000, blank=True)),
                ('favorite_animal', models.CharField(max_length=20, default='Dragons.')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='user_profile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
