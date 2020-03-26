from rest_framework import viewsets

from distributor.models import Hospital
from distributor.serializers import HospitalSerializer


class HospitalViewSet(viewsets.ModelViewSet):
    """
    API returns the list of the hospitals
    """
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
