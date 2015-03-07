from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    url(r'^login/', 'accounts.views.user_login'),
    url(r'^logout/', 'accounts.views.user_logout'),
    url(r'^register/', 'accounts.views.user_register'),

)
