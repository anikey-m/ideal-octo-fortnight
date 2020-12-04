from django.contrib import admin

from . import models


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created', 'changed', 'total', 'contractor', 'brief_text')
    search_fields = ('total', 'contractor', 'text')
