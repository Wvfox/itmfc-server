from django.urls import re_path

from .views import *

urlpatterns = [
    # re_path(r'^$', ),
    re_path(r'^application$', application_list),
    re_path(r'^application/(?P<pk>\d+)$', application_detail),
    re_path(r'^application/actual/(?P<operator_id>\d+)$', application_actual),
    re_path(r'^application/last/(?P<operator_tg_id>\d+)$', application_last),

    re_path(r'^button$', button_list),
    re_path(r'^button/(?P<pk>\d+)$', button_detail),
    re_path(r'^button/stud$', button_create_stud),
    re_path(r'^button/(?P<pk>\d+)/stud$', button_view_stud),
    re_path(r'^button/type/(?P<type_filter>[-.\w]+)$', button_type),
    re_path(r'^button/(?P<pk>\d+)/problem/(?P<problem_pk>\d+)$', button_problem),
]
