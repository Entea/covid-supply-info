from rest_framework import serializers

from distributor.models import Hospital, HospitalPhoneNumber


class HospitalPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalPhoneNumber
        fields = ['value']


class HospitalSerializer(serializers.HyperlinkedModelSerializer):
    phone_numbers = HospitalPhoneNumberSerializer(many=True, read_only=True)
    location = serializers.SerializerMethodField()

    class Meta:
        model = Hospital
        fields = ['name', 'code', 'address', 'location', 'phone_numbers']

    @staticmethod
    def get_location(obj):
        return {"longitude": obj.location.y, 'latitude': obj.location.x}
