from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',

    url(r'^markdown/', include('django_bootstrap_markdown.urls')),
    url(r'^login/',  'qishi.views_user.user_login'),
    url(r'^logout/', 'qishi.views_user.user_logout'),
    url(r'^register/', 'qishi.views_user.user_register'),
    url(r'^new_post/', 'qishi.views_forum.new_post'),
    url(r'^display_posts/', 'qishi.views_forum.display_posts'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'',  'qishi.views.home'), # back to homepage for all unmatched url
)
