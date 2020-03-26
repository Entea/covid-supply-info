from rest_framework import serializers

from distributor.models import Hospital, HospitalPhoneNumber, Donation, DonationDetail, NeedType, Measure


class HospitalPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalPhoneNumber
        fields = ['value']


class HospitalSerializer(serializers.HyperlinkedModelSerializer):
    phone_numbers = HospitalPhoneNumberSerializer(many=True, read_only=True)
    location = serializers.SerializerMethodField()

    class Meta:
        model = Hospital
        fields = ['id', 'name', 'code', 'address', 'location', 'phone_numbers']

    @staticmethod
    def get_location(obj):
        return {"longitude": obj.location.y, 'latitude': obj.location.x}


class MeasureTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measure
        fields = ['id', 'name']


class NeedTypeSerializer(serializers.ModelSerializer):
    measure = MeasureTypeSerializer()

    class Meta:
        model = NeedType
        fields = ['id', 'name', 'measure', 'price_per_piece']


class DonationDetailSerializer(serializers.ModelSerializer):
    need_type = NeedTypeSerializer(read_only=True)

    class Meta:
        model = DonationDetail
        fields = ['id', 'amount', 'need_type']


class DonationSerializer(serializers.HyperlinkedModelSerializer):
    details = DonationDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Donation
        fields = ['id', 'donator_name', 'donator_type', 'description', 'created_at', 'details']
