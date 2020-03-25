from django.contrib import admin
from rangefilter.filter import DateRangeFilter

from distributor.models import Measure, NeedType, Donation, DonationDetail


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

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Measure)
class NeedTypeAdmin(admin.ModelAdmin):
    pass


class DonationDetailInline(admin.TabularInline):
    model = DonationDetail

    def has_module_permission(self, request):
        return False


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    inlines = (DonationDetailInline,)

    search_fields = (
        'donator_name',
    )

    list_display = (
        '__str__',
        'donator_type',
        'created_at',
        'modified_at',
        'created_by',
        'modified_by',
    )

    list_filter = (
        'donator_type',
        ('created_at', DateRangeFilter),
    )

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_by', None) is None:
            obj.created_by = request.user
        obj.modified_by = request.user
        obj.save()
