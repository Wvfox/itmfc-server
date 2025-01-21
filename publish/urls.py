from django.urls import re_path

from .views import *

urlpatterns = [
    re_path(r'^$', clip_list),
    re_path(r'^shuffle$', clip_list_shuffle),
    re_path(r'^clip/(?P<pk>\d+)$', clip_detail),
    re_path(r'^nonstop/(?P<location>[-/.\w]+)$', nonstop_location),
    re_path(r'^submit$', clip_submit),
    re_path(r'^clip/(?P<pk>\d+)/check$', clip_check),
    re_path(r'^wrong', clip_wrong_list),
    re_path(r'^clip/(?P<pk>\d+)/wrong$', clip_wrong_check),

    re_path(r'^location$', location_list),
    re_path(r'^location/(?P<pk>\d+)/check$', location_check),
    re_path(r'^location/(?P<pk>\d+)', location_detail),


    # re_path(r'^(?P<pk>\d+)$', task_detail),
]
