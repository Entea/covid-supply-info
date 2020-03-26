from django.contrib import admin
from django.contrib.gis.db import models
from mapwidgets.widgets import GooglePointFieldWidget
from rangefilter.filter import DateRangeFilter
from modeltranslation.admin import TranslationAdmin

from distributor.models import Measure, NeedType, Donation, DonationDetail, Hospital, HospitalPhoneNumber, Region, District, Locality


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


@admin.register(Hospital)
class HospitalAdmin(TranslationAdmin):
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget}
    }

    inlines = (HospitalPhoneNumberInline,)

    search_fields = (
        'name',
        'code',
    )

    list_display = (
        'name',
        'code',
    )

@admin.register(Region)
class RegionAdmin(TranslationAdmin):
    pass

@admin.register(District)
class DistrictAdmin(TranslationAdmin):
    pass

@admin.register(Locality)
class LocalityAdmin(TranslationAdmin):
    pass