from django.contrib import admin, messages
from django.shortcuts import redirect
from django.urls import path, reverse_lazy
from django.utils.timezone import now
from leaflet.admin import LeafletGeoAdmin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from rangefilter.filter import DateRangeFilter
from django.utils.translation import ugettext as _

from distributor.models import (
    Measure, NeedType, Donation,
    DonationDetail, Hospital, HospitalPhoneNumber,
    Region, District, Locality,
    Statistic, StatisticCategory, HelpRequest,
    HospitalNeeds, Page, ContactInfo, ContactInfoPhoneNumber, ContactInfoEmail, ContactMessage, Distribution,
    DistributionDetail)


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
class HospitalAdmin(TranslationAdmin, LeafletGeoAdmin):
    change_list_template = 'admin/hospital_change_list.html'

    inlines = (HospitalPhoneNumberInline, NeedsInline, StatisticInline)

    readonly_fields = ('search_locality_id', 'search_district_id', 'search_region_id')

    search_fields = (
        'name',
        'code',
    )

    list_display = (
        'name',
        'code',
    )

    list_filter = (
        'hidden',
        'locality',
    )

    fieldsets_super_user = [
        (None, {'fields': ['name_ru',
                           'name_ky',
                           'code',
                           'address',
                           'location',
                           'locality',
                           'search_locality_id',
                           'search_district_id',
                           'search_region_id']}),
        (_('Дополнительные поля'), {
            'fields': ['managers', 'hidden'],
            'classes': ['collapse']
        }),
    ]

    fieldsets_user = [
        (None, {'fields': ['name_ru',
                           'name_ky',
                           'code',
                           'address',
                           'location',
                           'locality',
                           'search_locality_id',
                           'search_district_id',
                           'search_region_id']}),
    ]

    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            self.fieldsets = self.fieldsets_super_user
        else:
            self.fieldsets = self.fieldsets_user
        return super(HospitalAdmin, self).get_form(request, obj, **kwargs)

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(HospitalAdmin, self).get_queryset(request)
        return request.user.hospitals

    def get_urls(self):
        urls = super(HospitalAdmin, self).get_urls()
        my_urls = [
            path(r'hospital_update_search_fields',
                 self.admin_site.admin_view(self.update_hospital_search_fields), name="update_hospitals_search_fields"),
        ]
        return my_urls + urls

    @staticmethod
    def update_hospital_search_fields(request):
        try:
            hospitals = Hospital.objects.all()
            for hospital in hospitals:
                hospital.save()
            messages.add_message(request, messages.INFO, _("Search fields have been updated successfully"))
        except:
            messages.add_message(request, messages.ERROR, _("An error occurred during the updating search fields"))
        return redirect(reverse_lazy('admin:distributor_hospital_changelist'))

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


@admin.register(Page)
class PageAdmin(TranslationAdmin):
    search_fields = (
        'name',
        'url',
    )


class ContactInfoPhoneNumberInline(admin.TabularInline):
    model = ContactInfoPhoneNumber

    def has_module_permission(self, request):
        return False


class ContactInfoEmailInline(admin.TabularInline):
    model = ContactInfoEmail

    def has_module_permission(self, request):
        return False


@admin.register(ContactInfo)
class ContactInfoAdmin(TranslationAdmin):
    inlines = (ContactInfoPhoneNumberInline, ContactInfoEmailInline)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    readonly_fields = ('full_name', 'title', 'email', 'phone_number', 'body')

    search_fields = (
        'full_name',
        'title',
    )

    list_display = (
        'full_name',
        'title',
        'email',
        'phone_number',
        'created_at',
    )

    list_filter = (
        ('created_at', DateRangeFilter),
    )

    ordering = ('-created_at',)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return True


class DistributionDetailInline(admin.TabularInline):
    model = DistributionDetail

    def has_module_permission(self, request):
        return False


@admin.register(Distribution)
class DistributionAdmin(admin.ModelAdmin):
    inlines = (DistributionDetailInline,)

    exclude = ('created_at', 'updated_at')
    list_filter = (
        ('distributed_at', DateRangeFilter),
    )

    search_fields = ('sender', 'receiver')
    ordering = ('-created_at',)

    list_display = (
        'hospital',
        'donation',
        'sender',
        'receiver',
        'distributed_at'
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "hospital":
            # Отображаем только нескрытые больнички
            kwargs["queryset"] = Hospital.objects.filter(hidden=False)
            if request.user.hospitals.count() > 0:
                # Для старших медсестер отображаем только привязанные больницы
                kwargs["queryset"] = request.user.hospitals
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(DistributionDetail)
class DistributionDetailAdmin(admin.ModelAdmin):
    exclude = ('created_at', 'updated_at')
