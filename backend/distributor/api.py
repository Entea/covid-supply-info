from cacheops import cached_view_as
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from distributor.models import (
    Hospital, Donation, Region,
    District, Locality, HelpRequest,
    Page, ContactInfo, ContactMessage)
from distributor.serializers import (
    HospitalSerializer, DonationSerializer, RegionSerializer,
    DistrictSerializer, LocalitySerializer, HelpRequestSerializer,
    PageSerializer, HospitalShortInfoSerializer, HospitalDetailSerializer, ContactInfoSerializer,
    ContactMessageSerializer)
from distributor.services import HospitalService


class HospitalViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API returns the list of the hospitals
    """
    queryset = Hospital.objects.filter(hidden=False)
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


class PageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API returns the list of the pages
    """
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('url',)


class HospitalShortInfoListAPIView(ListAPIView):
    """
    API create hospital short info
    """
    queryset = Hospital.objects.filter(hidden=False)
    serializer_class = HospitalShortInfoSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('name',)
    filter_fields = ('search_locality_id', 'search_district_id', 'search_region_id')

    @method_decorator(cached_view_as(Hospital))
    def dispatch(self, *args, **kwargs):
        return super(HospitalShortInfoListAPIView, self).dispatch(*args, **kwargs)


class HospitalDetailAPIView(APIView):
    """
    API returns hospital details
    """
    serializer_class = HospitalDetailSerializer
    permission_classes = ()

    def get(self, request, pk):
        hospital = HospitalService.get(pk=pk)

        return Response(self.serializer_class(hospital).data)


class ContactInfoAPIView(APIView):
    """
    API returns contact info
    """
    serializer_class = ContactInfoSerializer
    permission_classes = ()

    def get(self, request):
        contact_info = ContactInfo.objects.first()
        return Response(self.serializer_class(contact_info).data)


class HelpRequestAPIView(APIView):
    """
    API creates help requests
    """
    permission_classes = ()
    authentication_classes = ()
    http_method_names = ['post', 'head']

    @staticmethod
    def post(request, *args, **kwargs):
        serializer = HelpRequestSerializer(data=request.data)
        if serializer.is_valid():
            HelpRequest.objects.create(
                first_name=serializer.data['first_name'],
                last_name=serializer.data['last_name'],
                locality=Locality.objects.get(pk=serializer.data['locality_id']),
                position=serializer.data['position'],
                hospital_name=serializer.data['hospital_name'],
                phone_number=serializer.data['phone_number'],
                description=serializer.data['description'],
            )
            return Response({'success': True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContactMessageAPIView(APIView):
    """
    API creates contact messages
    """
    permission_classes = ()
    authentication_classes = ()
    http_method_names = ['post', 'head']

    @staticmethod
    def post(request, *args, **kwargs):
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            ContactMessage.objects.create(
                full_name=serializer.data['full_name'],
                phone_number=serializer.data['phone_number'],
                email=serializer.data['email'],
                title=serializer.data['title'],
                body=serializer.data['body'],
            )
            return Response({'success': True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
