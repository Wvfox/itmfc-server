from django.urls import re_path

from .views import *

urlpatterns = [
    # re_path(r'^$', ),
    re_path(r'^application$', application_list),
    re_path(r'^application/(?P<pk>\d+)$', application_detail),

    re_path(r'^button$', button_list),
    re_path(r'^button/(?P<pk>\d+)$', button_detail),
    re_path(r'^button/type/(?P<type_filter>[-.\w]+)$', button_type),
    re_path(r'^button/(?P<pk>\d+)/problem/(?P<problem_pk>\d+)$', button_problem),
]
