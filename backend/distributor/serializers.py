from rest_framework import serializers

from distributor.models import (
    Hospital, HospitalPhoneNumber, Donation,
    DonationDetail, NeedType, Measure,
    Region, District, Locality,
    Statistic, HelpRequest, HospitalNeeds,
    Page)


class HospitalPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalPhoneNumber
        fields = ['value']


class StatisticPhoneNumberSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')

    class Meta:
        model = Statistic
        fields = ['category', 'actual', 'capacity', 'has_capacity', 'need_help']


class MeasureTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measure
        fields = ['id', 'name']


class NeedTypeSerializer(serializers.ModelSerializer):
    measure = MeasureTypeSerializer()

    class Meta:
        model = NeedType
        fields = ['id', 'name', 'measure']


class HospitalNeedsSerializer(serializers.ModelSerializer):
    need_type = NeedTypeSerializer(read_only=True)

    class Meta:
        model = HospitalNeeds
        fields = ['need_type', 'reserve_amount', 'request_amount', 'created_at']


class HospitalSerializer(serializers.HyperlinkedModelSerializer):
    phone_numbers = HospitalPhoneNumberSerializer(many=True, read_only=True)
    statistics = StatisticPhoneNumberSerializer(many=True, read_only=True)
    needs = HospitalNeedsSerializer(many=True, read_only=True)

    class Meta:
        model = Hospital
        fields = (
            'id', 'name', 'code', 'address',
            'full_location', 'locality_id', 'phone_numbers',
            'needs', 'statistics'
        )


class HospitalDetailSerializer(serializers.ModelSerializer):
    phone_numbers = HospitalPhoneNumberSerializer(many=True, read_only=True)
    statistics = StatisticPhoneNumberSerializer(many=True, read_only=True)
    needs = HospitalNeedsSerializer(many=True, read_only=True)

    class Meta:
        model = Hospital
        fields = ('id', 'phone_numbers', 'statistics', 'needs')


class HospitalShortInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ('id',
                  'name',
                  'full_location',
                  'code',
                  'search_locality_id',
                  'search_district_id',
                  'search_region_id',
                  'indicator')


class DonationDetailSerializer(serializers.ModelSerializer):
    need_type = NeedTypeSerializer(read_only=True)

    class Meta:
        model = DonationDetail
        fields = ['id', 'amount', 'need_type', 'price_per_piece']


class DonationSerializer(serializers.HyperlinkedModelSerializer):
    details = DonationDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Donation
        fields = ['id', 'donator_name', 'donator_type', 'description', 'created_at', 'details']


class RegionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name']


class DistrictSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'region_id', 'name']


class LocalitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Locality
        fields = ['id', 'district_id', 'name']


class HelpRequestSerializer(serializers.HyperlinkedModelSerializer):
    locality = LocalitySerializer(many=False, read_only=True)
    locality_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = HelpRequest
        fields = ['first_name', 'last_name', 'position', 'hospital_name', 'locality', 'locality_id', 'phone_number',
                  'description']
        read_only_fields = ['created_at', 'read_at']


class PageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Page
        fields = ['id', 'name', 'url', 'content']
