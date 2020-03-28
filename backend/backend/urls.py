"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls

from distributor import api

router = routers.DefaultRouter()
router.register(r'hospitals', api.HospitalViewSet)
router.register(r'donations', api.DonationViewSet)
router.register(r'regions', api.RegionViewSet)
router.register(r'districts', api.DistrictViewSet)
router.register(r'localities', api.LocalityViewSet)
router.register(r'help-requests', api.HelpRequestCreateViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^docs/', include_docs_urls(title='API Docs', public=False))
]
