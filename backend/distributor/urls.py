from django.urls import path
from rest_framework import routers

from distributor.api import (
    HospitalViewSet, DonationViewSet,
    RegionViewSet, DistrictViewSet, LocalityViewSet,
    PageViewSet, HospitalShortInfoListAPIView, HospitalDetailAPIView, ContactInfoAPIView,
    ContactMessageAPIView, HelpRequestAPIView, DistributionListAPIView, ManagerHospitalsListAPIView,
    ManagerDistributionListAPIView, DistributionDetailAPIView, HospitalNeedsListCreateAPIView,
    NeedTypesListCreateAPIView, MeasureListCreateAPIView)

router = routers.DefaultRouter()
router.register(r'hospitals', HospitalViewSet)
router.register(r'donations', DonationViewSet)
router.register(r'regions', RegionViewSet)
router.register(r'districts', DistrictViewSet)
router.register(r'localities', LocalityViewSet)
router.register(r'pages', PageViewSet)

urlpatterns = [
    path('all_hospitals/', HospitalShortInfoListAPIView.as_view(), name='all_hospitals'),
    path('hospitals/<int:pk>/details/', HospitalDetailAPIView.as_view(), name='hospital_detail'),
    path('contact-info/', ContactInfoAPIView.as_view(), name='contact_info'),
    path('contact-messages/', ContactMessageAPIView.as_view(), name='contact_message'),
    path('help-requests/', HelpRequestAPIView.as_view(), name='help_request'),
    path('distributions/', DistributionListAPIView.as_view(), name='distributions'),
    path('distributions/<int:pk>/', DistributionDetailAPIView.as_view(), name='distributions_detail'),
    path('managers/hospitals/', ManagerHospitalsListAPIView.as_view(), name='managers_hospital'),
    path('managers/distributions/', ManagerDistributionListAPIView.as_view(), name='managers_distributions'),
    path('hospital-needs/', HospitalNeedsListCreateAPIView.as_view(), name='hospital_needs'),
    path('need-types/', NeedTypesListCreateAPIView.as_view(), name='need_types'),
    path('measures/', MeasureListCreateAPIView.as_view(), name='measures'),
]

urlpatterns += router.urls
