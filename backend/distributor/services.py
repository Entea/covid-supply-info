import os

import requests
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from rest_framework.exceptions import NotFound

from distributor.models import Hospital

User = get_user_model()


class HospitalService:
    model = Hospital

    @classmethod
    def get(cls, **filters):
        try:
            return Hospital.objects.get(**filters)
        except Hospital.DoesNotExist:
            raise NotFound('Hospital not found')

    @classmethod
    def get_managers_hospitals(cls, user: User) -> QuerySet:
        return Hospital.objects.filter(managers__in=[user])


class GooglePlaceAPI:
    GOOGLE_PLACE_API_URL = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json'

    @classmethod
    def find_locations(cls, search):
        params = {'input': f'{search}',
                  'inputtype': 'textquery',
                  'fields': 'name,geometry',
                  'key': os.environ.get("MAP_API_KEY")}

        response = requests.get(cls.GOOGLE_PLACE_API_URL, params=params).json()

        locations = [{'lng': candidate["geometry"]["location"]["lng"],
                      'lat': candidate["geometry"]["location"]["lat"]} for candidate in response["candidates"]]

        return locations
