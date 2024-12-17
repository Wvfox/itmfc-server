from django.contrib import admin
from django.urls import path, include, re_path

from config.utilities import get_src_file

urlpatterns = [
    path('admin/', admin.site.urls),

    re_path(r'^api/file/(?P<media_url>[-/.\w]+)$', get_src_file),

    path('api/task/', include('task.urls')),
    path('api/personal/', include('personal.urls')),
    path('api/helpdesk/', include('helpdesk.urls')),
    path('api/publish/', include('publish.urls'))
]
