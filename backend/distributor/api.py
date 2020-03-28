from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from distributor.models import (
    Hospital, Donation, Region,
    District, Locality, HelpRequest,
    Page)
from distributor.serializers import (
    HospitalSerializer, DonationSerializer, RegionSerializer,
    DistrictSerializer, LocalitySerializer, HelpRequestSerializer,
    PageSerializer)


class HospitalViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API returns the list of the hospitals
    """
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('name',)
    filter_fields = ('locality',)


class DonationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API returns the list of the donations
    """
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer


class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API returns the list of the regions
    """
    queryset = Region.objects.all().order_by('name')
    serializer_class = RegionSerializer


class DistrictViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API returns the list of the districts
    """
    queryset = District.objects.all().order_by('name')
    serializer_class = DistrictSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('region',)


class LocalityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API returns the list of the localities
    """
    queryset = Locality.objects.all().order_by('name')
    serializer_class = LocalitySerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('district',)


class HelpRequestCreateViewSet(viewsets.ModelViewSet):
    """
    API create help requests
    """
    queryset = HelpRequest.objects.all()
    serializer_class = HelpRequestSerializer
    permission_classes = ()
    authentication_classes = ()
    http_method_names = ['post', 'head']


class PageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API returns the list of the pages
    """
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('url',)
