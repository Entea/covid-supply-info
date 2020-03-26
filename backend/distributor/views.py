from rest_framework import viewsets

from distributor.models import Hospital, Donation, Region, District, Locality
from distributor.serializers import HospitalSerializer, DonationSerializer, RegionSerializer, DistrictSerializer, \
    LocalitySerializer


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


class RegionViewSet(viewsets.ModelViewSet):
    """
    API returns the list of the regions
    """
    queryset = Region.objects.all().order_by('name')
    serializer_class = RegionSerializer


class DistrictViewSet(viewsets.ModelViewSet):
    """
    API returns the list of the districts
    """
    queryset = District.objects.all().order_by('name')
    serializer_class = DistrictSerializer


class LocalityViewSet(viewsets.ModelViewSet):
    """
    API returns the list of the localities
    """
    queryset = Locality.objects.all().order_by('name')
    serializer_class = LocalitySerializer
