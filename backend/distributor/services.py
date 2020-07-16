import os
from typing import Union

import requests
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from rest_framework.exceptions import NotFound, ValidationError

from .models import Hospital, Distribution, HospitalNeeds, NeedType, Measure

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


class DistributionService:
    model = Distribution

    @classmethod
    def get(cls, **filters):
        try:
            return cls.model.objects.get(**filters)
        except cls.model.DoesNotExist:
            raise NotFound('Distribution not found')

    @classmethod
    def filter(cls, **filters):
        return cls.model.objects.filter(**filters)

    @classmethod
    def get_manager_hospitals_distributions(cls, user: User):
        return cls.filter(hospital__managers__in=[user])


class MeasureService:
    model = Measure

    @classmethod
    def get(cls, **filters):
        try:
            return cls.model.objects.get(**filters)
        except cls.model.DoesNotExist:
            raise NotFound('Measure not found')

    @classmethod
    def filter(cls, **filters):
        return cls.model.objects.filter(**filters)

    @classmethod
    def create(cls, name: str) -> model:
        try:
            return cls.model.objects.create(
                name=name
            )
        except Exception as e:
            raise ValidationError('Error while creating Measure: {e}'.format(e=str(e)))


class NeedTypeService:
    model = NeedType

    @classmethod
    def get(cls, **filters):
        try:
            return cls.model.objects.get(**filters)
        except cls.model.DoesNotExist:
            raise NotFound('NeedType not found')

    @classmethod
    def filter(cls, **filters):
        return cls.model.objects.filter(**filters)

    @classmethod
    def create(cls, user: User, measure_id: Union[int, None], name: str) -> model:
        measure = None
        if measure_id is not None:
            measure = MeasureService.get(id=measure_id)
        try:
            return cls.model.objects.create(
                name=name,
                measure=measure,
                created_by=user,
                modified_by=user
            )
        except Exception as e:
            raise ValidationError('Error while creating need type: {e}'.format(e=str(e)))


class HospitalNeedsService:
    model = HospitalNeeds

    @classmethod
    def get(cls, **filters):
        try:
            return cls.model.objects.get(**filters)
        except cls.model.DoesNotExist:
            raise NotFound('Needs not found')

    @classmethod
    def filter(cls, **filters):
        return cls.model.objects.filter(**filters)

    @classmethod
    def get_manager_hospitals_needs(cls, user: User):
        return cls.filter(hospital__managers__in=[user])

    @classmethod
    def create(cls, hospital_id: int, need_type_id: int, reserve_amount: int,
               request_amount: int, request_amount_month: int) -> model:
        try:

            hospital = HospitalService.get(id=hospital_id)
            need_type = NeedTypeService.get(id=need_type_id)

            return cls.model.objects.create(
                hospital=hospital,
                need_type=need_type,
                reserve_amount=reserve_amount,
                request_amount=request_amount,
                request_amount_month=request_amount_month
            )
        except Exception as e:
            raise ValidationError('Error while creating hospital needs: {e}'.format(e=str(e)))
