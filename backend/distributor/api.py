from cacheops import cached_view_as
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from distributor.models import (
    Hospital, Donation, Region,
    District, Locality, HelpRequest,
    Page)
from distributor.serializers import (
    HospitalSerializer, DonationSerializer, RegionSerializer,
    DistrictSerializer, LocalitySerializer, HelpRequestSerializer,
    PageSerializer, HospitalShortInfoSerializer, HospitalDetailSerializer)
from distributor.services import HospitalService


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
    pagination_class = None
    serializer_class = RegionSerializer

    @method_decorator(cached_view_as(Region))
    def dispatch(self, *args, **kwargs):
        return super(RegionViewSet, self).dispatch(*args, **kwargs)


class DistrictViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API returns the list of the districts
    """
    queryset = District.objects.all().order_by('name')
    serializer_class = DistrictSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    filter_fields = ('region',)

    @method_decorator(cached_view_as(District))
    def dispatch(self, *args, **kwargs):
        return super(DistrictViewSet, self).dispatch(*args, **kwargs)


class LocalityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API returns the list of the localities
    """
    queryset = Locality.objects.all().order_by('name')
    serializer_class = LocalitySerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    filter_fields = ('district',)

    @method_decorator(cached_view_as(Locality))
    def dispatch(self, *args, **kwargs):
        return super(LocalityViewSet, self).dispatch(*args, **kwargs)


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


class HospitalShortInfoListAPIView(ListAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalShortInfoSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('name',)
    filter_fields = ('search_locality_id', 'search_district_id', 'search_region_id')

    @method_decorator(cached_view_as(Hospital))
    def dispatch(self, *args, **kwargs):
        return super(HospitalShortInfoListAPIView, self).dispatch(*args, **kwargs)


class HospitalDetailAPIView(APIView):
    serializer_class = HospitalDetailSerializer
    permission_classes = ()

    def get(self, request, pk):
        hospital = HospitalService.get(pk=pk)

        return Response(self.serializer_class(hospital).data)
