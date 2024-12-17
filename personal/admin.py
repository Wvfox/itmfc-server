from django.contrib import admin

from .models import *


@admin.register(Operator)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'tag', 'birthday',
        'is_head', 'date_ecp',
        'updated_at', 'created_at'
    )
    list_filter = ('id', 'created_at')



