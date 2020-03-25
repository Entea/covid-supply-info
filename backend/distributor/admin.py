from django.contrib import admin
from rangefilter.filter import DateRangeFilter

from distributor.models import Measure, NeedType


@admin.register(NeedType)
class NeedAdmin(admin.ModelAdmin):
    search_fields = (
        'name',
    )

    list_display = (
        '__str__',
        'measure',
        'created_at',
        'modified_at',
        'created_by',
        'modified_by',
    )

    list_filter = (
        ('created_at', DateRangeFilter),
    )

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_by', None) is None:
            obj.created_by = request.user
        obj.modified_by = request.user
        obj.save()


@admin.register(Measure)
class NeedTypeAdmin(admin.ModelAdmin):
    pass
