from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',

    #url(r'^$', 'test_app.views.test_view'),
    url(r'^home/',  'qishi.views.home'),
    url(r'^markdown/', include('django_bootstrap_markdown.urls')),
    url(r'^login/',  'qishi.views_user.user_login'),
    url(r'^logout/', 'qishi.views_user.user_logout'),
    url(r'^new_post/', 'qishi.views_forum.new_post'),
    url(r'^display_post/', 'qishi.views_forum.display_post'),
    url(r'^admin/', include(admin.site.urls)),
)
