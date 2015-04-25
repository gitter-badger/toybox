# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('qishi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='liked_by',
            field=models.ManyToManyField(blank=True, related_name='topics_liked', null=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='topic',
            name='mainpost',
            field=models.ForeignKey(blank=True, verbose_name='Mainpost', null=True, related_name='topics', to='qishi.Post'),
            preserve_default=True,
        ),
    ]
