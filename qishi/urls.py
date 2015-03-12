from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    url(r'^categories/$', 'qishi.views_forum.category'),
    url(r'^markdown/', include('django_bootstrap_markdown.urls')),
    url(r'^forum(?P<forum_id>\d+)/new_post/$', 'qishi.views_forum.new_post'),
    url(r'^forum(?P<forum_id>\d+)/$', 'qishi.views_forum.display_forum'),
    url(r'^(?P<topic_id>\d+)$','qishi.views_forum.topic'),
    url(r'^(?P<topic_id>\d+)/delete/$', 'qishi.views_forum.delete_topic',
        name='qishi_delete_topic'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'',  'qishi.views.home'), # back to homepage for all unmatched url
)
