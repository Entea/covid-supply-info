from django.contrib import admin
from django.contrib.gis.db import models
from django.utils.timezone import now
from mapwidgets.widgets import GooglePointFieldWidget
from modeltranslation.admin import TranslationAdmin
from rangefilter.filter import DateRangeFilter

from distributor.models import (
    Measure, NeedType, Donation,
    DonationDetail, Hospital, HospitalPhoneNumber,
    Region, District, Locality,
    Statistic, StatisticCategory, HelpRequest,
    HospitalNeeds
)



@admin.register(NeedType)
class NeedTypeAdmin(TranslationAdmin):
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
class MeasureAdmin(TranslationAdmin):
    pass


class DonationDetailInline(admin.TabularInline):
    model = DonationDetail

    def has_module_permission(self, request):
        return False


@admin.register(Donation)
class DonationAdmin(TranslationAdmin):
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


class HospitalPhoneNumberInline(admin.TabularInline):
    model = HospitalPhoneNumber

    def has_module_permission(self, request):
        return False


class StatisticInline(admin.TabularInline):
    model = Statistic
    extra = 1

    def has_module_permission(self, request):
        return False


class NeedsInline(admin.TabularInline):
    model = HospitalNeeds

    def has_module_permission(self, request):
        return False


@admin.register(Hospital)
class HospitalAdmin(TranslationAdmin):
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget}
    }

    inlines = (HospitalPhoneNumberInline, NeedsInline, StatisticInline)

    search_fields = (
        'name',
        'code',
    )

    list_display = (
        'name',
        'code',
    )

    class Media:
        js = (
            "js/statistic.js",
        )
        css = {
            'all': ("css/statistic.css",)
        }


@admin.register(Region)
class RegionAdmin(TranslationAdmin):
    pass


@admin.register(District)
class DistrictAdmin(TranslationAdmin):
    list_filter = (
        'region',
    )


@admin.register(Locality)
class LocalityAdmin(TranslationAdmin):
    list_filter = (
        'district',
    )


@admin.register(StatisticCategory)
class StatisticCategoryAdmin(TranslationAdmin):
    pass


@admin.register(HelpRequest)
class HelpRequestAdmin(admin.ModelAdmin):
    search_fields = (
        'first_name',
        'last_name',
    )

    list_display = (
        'first_name',
        'last_name',
        'position',
        'phone_number',
        'locality',
        'created_at',
        'read_at',
        'is_read',
    )

    list_filter = (
        'is_read',
        ('created_at', DateRangeFilter),
    )

    ordering = ('-created_at',)

    def get_object(self, request, object_id, from_field=None):
        obj = super(HelpRequestAdmin, self).get_object(request, object_id)
        if obj and not obj.is_read:
            obj.is_read = True
            obj.save()
        if obj and not obj.read_at:
            obj.read_at = now()
            obj.save()
        return obj
