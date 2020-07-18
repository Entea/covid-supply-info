from cacheops import cached_view_as
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from distributor.filters import DistributionFilter
from distributor.models import (
    Hospital, Donation, Region,
    District, Locality, HelpRequest,
    Page, ContactInfo, ContactMessage, Distribution)
from distributor.serializers import (
    HospitalSerializer, DonationSerializer, RegionSerializer,
    DistrictSerializer, LocalitySerializer, HelpRequestSerializer,
    PageSerializer, HospitalShortInfoSerializer, HospitalDetailSerializer, ContactInfoSerializer,
    ContactMessageSerializer, DistributionListSerializer, DistributionShortListSerializer, NeedsSerializer,
    NeedsCreateSerializer, NeedTypeSerializer, NeedTypeCreateSerializer,
    MeasureTypeSerializer, MeasureCreateSerializer
)
from .services import (
    HospitalService, DistributionService, HospitalNeedsService,
    NeedTypeService, MeasureService
)


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
    queryset = Donation.objects.all().order_by('-created_at')
    pagination_class = None
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
        serializer.is_valid(raise_exception=True)

        ContactMessage.objects.create(
            full_name=serializer.validated_data.get('full_name'),
            phone_number=serializer.validated_data.get('phone_number'),
            email=serializer.validated_data.get('email'),
            title=serializer.validated_data.get('title'),
            body=serializer.validated_data.get('body'),
        )

        return Response({'success': True}, status=status.HTTP_201_CREATED)


class DistributionListAPIView(ListAPIView):
    """
    List API to show distribution objects
    """
    permission_classes = ()
    authentication_classes = ()
    serializer_class = DistributionListSerializer
    queryset = Distribution.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_class = DistributionFilter


class ManagerHospitalsListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = HospitalShortInfoSerializer

    def get_queryset(self):
        return HospitalService.get_managers_hospitals(user=self.request.user)


class ManagerDistributionListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = DistributionShortListSerializer

    def get_queryset(self):
        return DistributionService.get_manager_hospitals_distributions(user=self.request.user)


class DistributionDetailAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = DistributionListSerializer

    def get(self, request, pk):
        distribution = DistributionService.get(pk=pk)

        return Response(self.serializer_class(distribution, many=False).data, status=status.HTTP_200_OK)


class HospitalNeedsListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = NeedsSerializer

    def get_queryset(self):
        return HospitalNeedsService.get_manager_hospitals_needs(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = NeedsCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(data={
                'message': 'Invalid input',
                'errors': serializer.errors
            }, status=status.HTTP_406_NOT_ACCEPTABLE)

        hospital_need = HospitalNeedsService.create(**serializer.validated_data)

        return Response(self.serializer_class(hospital_need, many=False).data, status=status.HTTP_201_CREATED)


class NeedTypesListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = NeedTypeSerializer
    queryset = NeedTypeService.filter()

    def create(self, request, *args, **kwargs):
        serializer = NeedTypeCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(data={
                'message': 'Invalid input',
                'errors': serializer.errors
            }, status=status.HTTP_406_NOT_ACCEPTABLE)

        need_type = NeedTypeService.create(
            user=request.user,
            name=serializer.validated_data.get('name'),
            measure_id=serializer.validated_data.get('measure_id')
        )

        return Response(self.serializer_class(need_type, many=False).data, status=status.HTTP_201_CREATED)


class MeasureListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = MeasureTypeSerializer
    queryset = MeasureService.filter()

    def create(self, request, *args, **kwargs):
        serializer = MeasureCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(data={
                'message': 'Invalid input',
                'errors': serializer.errors
            }, status=status.HTTP_406_NOT_ACCEPTABLE)

        measure = MeasureService.create(
            name=serializer.validated_data.get('name')
        )

        return Response(self.serializer_class(measure, many=False).data, status=status.HTTP_201_CREATED)
