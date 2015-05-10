from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    url(r'^login/$', 'qishi.views_user.user_login'),
    url(r'^register/$', 'qishi.views_user.user_register'),
    url(r'^forum(?P<forum_id>\d+)/new_post/$', 'qishi.views_forum.new_post'),
    url(r'^(?P<topic_id>\d+)/new_reply/$', 'qishi.views_forum.new_reply'),
    url(r'^forum(?P<forum_id>\d+)/$', 'qishi.views_forum.display_forum'),
    url(r'^(?P<topic_id>\d+)$','qishi.views_forum.topic'),
    url(r'^(?P<topic_id>\d+)/delete/$', 'qishi.views_forum.delete_topic', name='qishi_delete_topic'),
    url(r'^post(?P<post_id>\d+)/like_switch/$', 'qishi.views_forum.like_post_switch', name='qishi_like_post_switch'),
    url(r'^(?P<topic_id>\d+)/update_topic_attr_switch/(?P<attr>[\w-]+)/$', 'qishi.views_forum.update_topic_attr_switch'),
    url(r'^post(?P<post_id>\d+)/delete/$', 'qishi.views_forum.delete_post',name='qishi_delete_post'),
    url(r'^post(?P<post_id>\d+)/edit/$', 'qishi.views_forum.edit_post',name='qishi_edit_post'),
    url(r'^blog/$','qishi.views_forum.blog'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'',  'qishi.views.home'), # back to homepage for all unmatched url
)
