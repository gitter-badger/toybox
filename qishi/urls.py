from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',

    url(r'^markdown/', include('django_bootstrap_markdown.urls')),
    url(r'^new_post/', 'qishi.views_forum.new_post'),
    url(r'^display_posts/', 'qishi.views_forum.display_posts'),
    url(r'^(?P<post_id>\d+)/delete/$', 'qishi.views_forum.delete_post',
        name='qishi_delete_post'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'',  'qishi.views.home'), # back to homepage for all unmatched url
)
