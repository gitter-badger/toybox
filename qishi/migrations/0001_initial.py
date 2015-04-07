# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(default='')),
                ('ordering', models.PositiveIntegerField(default=1)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ('-ordering', 'created_on'),
                'verbose_name': 'Category',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(default='')),
                ('ordering', models.PositiveIntegerField(default=1)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(null=True, blank=True)),
                ('category', models.ForeignKey(to='qishi.Category')),
                ('groups', models.ManyToManyField(null=True, to='auth.Group', verbose_name='Groups', help_text='Only users from these groups can see this category', blank=True)),
            ],
            options={
                'verbose_name_plural': 'Forums',
                'ordering': ('-ordering', '-created_on'),
                'verbose_name': 'Forum',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('message', models.TextField()),
                ('topic_post', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(null=True, blank=True)),
                ('posted_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Posts',
                'ordering': ('-created_on',),
                'verbose_name': 'Post',
                'get_latest_by': ('created_on',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('subject', models.CharField(max_length=999)),
                ('num_views', models.IntegerField(default=0)),
                ('num_replies', models.PositiveSmallIntegerField(default=0)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(null=True, blank=True)),
                ('closed', models.BooleanField(default=False)),
                ('sticky', models.BooleanField(default=False)),
                ('is_blog', models.BooleanField(default=False)),
                ('num_likes', models.IntegerField(default=0)),
                ('forum', models.ForeignKey(to='qishi.Forum', verbose_name='Forum')),
                ('posted_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Topics',
                'ordering': ('created_on',),
                'verbose_name': 'Topic',
                'get_latest_by': 'created_on',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='post',
            name='topic',
            field=models.ForeignKey(to='qishi.Topic', verbose_name='Topic', related_name='posts'),
            preserve_default=True,
        ),
    ]
