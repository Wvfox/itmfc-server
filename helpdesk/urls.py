from django.urls import re_path

from .views import *

urlpatterns = [
    # re_path(r'^$', ),
    re_path(r'^application$', application_list),
    re_path(r'^application/(?P<pk>\d+)$', application_detail),
]
