from django.contrib import admin
from django.utils.translation import ugettext as _

from distributor.models import Region, District, Locality


class RegionFilter(admin.SimpleListFilter):
    parameter_name = 'region_id'
    title = _("Регион")

    def lookups(self, request, model_admin):
        return map(lambda region: (region.pk, region.__str__()), Region.objects.all())

    def queryset(self, request, queryset):
        region_id = request.GET.get('region_id')
        if not region_id:
            return queryset.all()
        return queryset.filter(search_region_id=region_id)

    def choices(self, changelist):
        yield {
            'selected': self.value() is None,
            'query_string': changelist.get_query_string(remove=[self.parameter_name, 'locality_id', 'district_id']),
            'display': _('All'),
        }
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == str(lookup),
                'query_string': changelist.get_query_string(new_params={self.parameter_name: lookup},
                                                            remove=['locality_id', 'district_id']),
                'display': title,
            }


class DistrictFilter(admin.SimpleListFilter):
    parameter_name = 'district_id'
    title = _("Район")

    def lookups(self, request, model_admin):
        region_id = request.GET.get('region_id')
        if not region_id:
            return None
        return map(lambda district: (district.pk, district.name), District.objects.filter(region=region_id))

    def queryset(self, request, queryset):
        district_id = request.GET.get('district_id')
        if not district_id:
            return None
        return queryset.filter(search_district_id=district_id)

    def choices(self, changelist):
        yield {
            'selected': self.value() is None,
            'query_string': changelist.get_query_string(remove=[self.parameter_name, 'locality_id']),
            'display': _('All'),
        }
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == str(lookup),
                'query_string': changelist.get_query_string(new_params={self.parameter_name: lookup},
                                                            remove=['locality_id']),
                'display': title,
            }


class LocalityFilter(admin.SimpleListFilter):
    parameter_name = 'locality_id'
    title = _("Местность")

    def lookups(self, request, model_admin):
        district_id = request.GET.get('district_id')
        if not district_id:
            return None
        return map(lambda locality: (locality.pk, locality.name), Locality.objects.filter(district=district_id))

    def queryset(self, request, queryset):
        locality_id = request.GET.get(self.parameter_name)
        if not locality_id:
            return None
        return queryset.filter(search_locality_id=locality_id)
