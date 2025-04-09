from django.urls import re_path

from .views import *

urlpatterns = [
    re_path(r'^check/(?P<hostname>[-/.\w]+)/(?P<user>[-/.\w]+)$', check),
    re_path(r'^$', task_list),
    re_path(r'^(?P<pk>\d+)$', task_detail),
    re_path(r'^(?P<pk>\d+)/processing$', task_processing),
    re_path(r'^(?P<pk>\d+)/complete$', task_complete),

    re_path(r'^bot/start$', start_bot),
]
