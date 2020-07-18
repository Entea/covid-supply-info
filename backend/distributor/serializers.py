from rest_framework import serializers
from rest_framework_recaptcha.fields import ReCaptchaField

from .constants import (
    DISTRIBUTION_STATUSES, DONATOR_TYPES, ORGANIZATION
)
from .models import (
    Hospital, HospitalPhoneNumber, Donation,
    DonationDetail, NeedType, Measure,
    Region, District, Locality,
    Statistic, HospitalNeeds, Page,
    ContactInfo, ContactInfoPhoneNumber, ContactInfoEmail,
    Distribution, DistributionDetail
)


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
        fields = ['id', 'amount', 'need_type', 'total_cost']


class DonationSerializer(serializers.HyperlinkedModelSerializer):
    details = DonationDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Donation
        fields = ['id',
                  'donator_name',
                  'donator_type',
                  'total_price',
                  'total_donation',
                  'description',
                  'created_at',
                  'details'
                  ]


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


class PageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Page
        fields = ['id', 'name', 'url', 'content']


class ContactInfoPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfoPhoneNumber
        fields = ['value', 'is_whats_app']


class ContactInfoEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfoEmail
        fields = ['value']


class ContactInfoSerializer(serializers.HyperlinkedModelSerializer):
    phone_numbers = ContactInfoPhoneNumberSerializer(many=True, read_only=True)
    emails = ContactInfoEmailSerializer(many=True, read_only=True)

    class Meta:
        model = ContactInfo
        fields = ['text_ru', 'text_ky', 'phone_numbers', 'emails']


class HelpRequestSerializer(serializers.Serializer):
    recaptcha = ReCaptchaField()
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    position = serializers.CharField(max_length=50)
    hospital_name = serializers.CharField(max_length=250)
    locality_id = serializers.IntegerField(allow_null=False)
    phone_number = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=500)


class ContactMessageSerializer(serializers.Serializer):
    recaptcha = ReCaptchaField()
    full_name = serializers.CharField(max_length=100)
    phone_number = serializers.CharField(max_length=50)
    email = serializers.EmailField(max_length=100)
    title = serializers.CharField(max_length=100)
    body = serializers.CharField(max_length=400)


class DistributionDetailSerializer(serializers.ModelSerializer):
    need_type = NeedTypeSerializer()

    class Meta:
        model = DistributionDetail
        fields = ('id', 'need_type', 'total_cost', 'amount')


class DistributionListSerializer(serializers.ModelSerializer):
    hospital = HospitalShortInfoSerializer()
    details = DistributionDetailSerializer(many=True, source='distribution_details')

    class Meta:
        model = Distribution
        fields = (
            'id', 'hospital', 'details',
            'sender', 'receiver', 'distributed_at',
            'status', 'created_at', 'delivered_at'
        )


class DistributionShortListSerializer(DistributionListSerializer):
    class Meta:
        model = Distribution
        fields = (
            'id', 'hospital',
            'sender', 'receiver', 'distributed_at',
            'status', 'created_at', 'delivered_at'
        )


class NeedsSerializer(serializers.ModelSerializer):
    need_type = NeedTypeSerializer()
    hospital = HospitalShortInfoSerializer()

    class Meta:
        model = HospitalNeeds
        fields = ('need_type', 'hospital', 'reserve_amount', 'request_amount', 'created_at')


class NeedsCreateSerializer(serializers.Serializer):
    hospital_id = serializers.IntegerField()
    need_type_id = serializers.IntegerField()
    reserve_amount = serializers.IntegerField()
    request_amount = serializers.IntegerField()
    request_amount_month = serializers.IntegerField()


class NeedTypeCreateSerializer(serializers.Serializer):
    measure_id = serializers.IntegerField(allow_null=True)
    name = serializers.CharField()


class MeasureCreateSerializer(serializers.Serializer):
    name = serializers.CharField()


class DistributionCreateSerializer(serializers.Serializer):
    hospital_id = serializers.IntegerField()
    donation_id = serializers.IntegerField()
    sender = serializers.CharField()
    receiver = serializers.CharField()
    distributed_at = serializers.DateField()
    delivered_at = serializers.DateField(allow_null=True)
    status = serializers.ChoiceField(choices=DISTRIBUTION_STATUSES)


class DonationCreateSerializer(serializers.Serializer):
    donator_type = serializers.ChoiceField(choices=DONATOR_TYPES, default=ORGANIZATION)
    donator_name = serializers.CharField()
    total_price = serializers.CharField(allow_null=True)
    description = serializers.CharField()


class DonationDetailCreateSerializer(serializers.Serializer):
    need_type_id = serializers.IntegerField()
    amount = serializers.IntegerField()
    donation_id = serializers.IntegerField()
    total_cost = serializers.DecimalField(allow_null=True, decimal_places=2, max_digits=20)
