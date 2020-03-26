from rest_framework import viewsets

from distributor.models import Hospital, Donation
from distributor.serializers import HospitalSerializer, DonationSerializer


class HospitalViewSet(viewsets.ModelViewSet):
    """
    API returns the list of the hospitals
    """
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer


class DonationViewSet(viewsets.ModelViewSet):
    """
    API returns the list of the donations
    """
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
