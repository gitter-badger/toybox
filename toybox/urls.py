from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',

    #url(r'^$', 'test_app.views.test_view'),
    url(r'^home/',  'qishi.views.home'),
    url(r'^qishi/', include("qishi.urls")),
    url(r'^accounts/', include("accounts.urls")),

)
