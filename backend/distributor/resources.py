from import_export import resources, fields
from .models import Hospital


class HospitalResource(resources.ModelResource):
    phone_numbers = fields.Field()

    class Meta:
        model = Hospital
        use_transactions = True
        fields = (
            'name', 'code', 'address',
            'phone_numbers'
        )

    @staticmethod
    def dehydrate_phone_numbers(hospital):
        phone_numbers = list(hospital.phone_numbers.all())
        return ','.join([phone_number.value for phone_number in phone_numbers])
