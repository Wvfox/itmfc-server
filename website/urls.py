from django.urls import re_path

from .views import *

urlpatterns = [
    # re_path(r'^$', views.index, name='index'),
    re_path(r'^vacancy$', send_vacancy),
]
