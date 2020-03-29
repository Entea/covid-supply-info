from rest_framework.exceptions import NotFound

from distributor.models import Hospital


class HospitalService:
    model = Hospital

    @classmethod
    def get(cls, **filters):
        try:
            return Hospital.objects.get(**filters)
        except Hospital.DoesNotExist:
            raise NotFound('Hospital not found')
