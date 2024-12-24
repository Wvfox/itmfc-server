from django.urls import re_path

from .views import *

urlpatterns = [
    # re_path(r'^$', views.index, name='index'),
    re_path(r'^operator$', operator_list),
    re_path(r'^operator/(?P<pk>\d+)$', operator_detail),
    re_path(r'^operator/username/(?P<username>[-.\w]+)$', operator_detail),
    re_path(r'^operator/tg-id/(?P<tg_id>\d+)$', operator_detail),
    re_path(r'^operator/tag/(?P<tag>[-.\w]+)$', operator_detail),
    re_path(r'^operator/birthday$', operator_birthday),
    re_path(r'^printer$', printer_list),
    re_path(r'^printer/(?P<ip>[-.\w]+)$', printer_detail),
    re_path(r'^workstation$', workstation_list),
    re_path(r'^workstation/(?P<name>[-.\w]+)$', workstation_detail),
    re_path(r'^workstation/(?P<name>[-.\w]+)/printer/(?P<ip>[-.\w]+)$', workstation_printer),
]
