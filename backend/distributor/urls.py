from django.urls import path
from rest_framework import routers

from distributor.api import (
    HospitalViewSet, DonationViewSet,
    RegionViewSet, DistrictViewSet, LocalityViewSet,
    HelpRequestCreateViewSet,
    PageViewSet, HospitalShortInfoListAPIView)

router = routers.DefaultRouter()
router.register(r'hospitals', HospitalViewSet)
router.register(r'donations', DonationViewSet)
router.register(r'regions', RegionViewSet)
router.register(r'districts', DistrictViewSet)
router.register(r'localities', LocalityViewSet)
router.register(r'help-requests', HelpRequestCreateViewSet)
router.register(r'pages', PageViewSet)

urlpatterns = [
    path('all_hospitals', HospitalShortInfoListAPIView.as_view(), name='all_hospitals')
]

urlpatterns += router.urls
