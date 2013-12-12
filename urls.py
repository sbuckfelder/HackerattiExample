from django.conf.urls import patterns, include, url
from views import graphAndTable

urlpatterns = patterns('',
    url(r'^main/$', graphAndTable),
)
