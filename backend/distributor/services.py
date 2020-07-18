import os
from typing import Union

import requests
from django.contrib.auth import get_user_model
from django.db.models import QuerySet, Q
from rest_framework.exceptions import NotFound, ValidationError

from .models import (
    Hospital, Distribution,
    HospitalNeeds, NeedType,
    Measure, Donation,
    DonationDetail
)

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

    @classmethod
    def create(cls, hospital: Hospital, donation: Donation, sender: str, receiver: str,
               distributed_at: str, delivered_at: str, status: str):
        try:
            return cls.model.objects.create(
                hospital=hospital,
                donation=donation,
                sender=sender,
                receiver=receiver,
                distributed_at=distributed_at,
                delivered_at=delivered_at,
                status=status
            )
        except Exception as e:
            raise ValidationError('Error while creating distributions: {e}'.format(e=str(e)))


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


class DonationService:
    model = Donation

    @classmethod
    def get(cls, **filters):
        try:
            return cls.model.objects.get(**filters)
        except cls.model.DoesNotExist:
            raise NotFound('Donation not found')

    @classmethod
    def get_donation_detail(cls, **filters):
        try:
            return DonationDetail.objects.get(**filters)
        except DonationDetail.DoesNotExist:
            raise NotFound('DonationDetail not found')

    @classmethod
    def create(cls, donator_type: str, donator_name: str, total_price: Union[str, None],
               description: str, created_by: User, modified_by: User):
        try:
            return cls.model.objects.create(
                donator_type=donator_type,
                donator_name=donator_name,
                total_price=total_price,
                description=description,
                created_by=created_by,
                modified_by=modified_by
            )
        except Exception as e:
            raise ValidationError('Error while creating donation: {e}'.format(e=str(e)))

    @classmethod
    def get_manager_donations(cls, user: User) -> QuerySet:
        return cls.model.objects.filter(
            Q(created_by=user) | Q(modified_by=user)
        )

    @classmethod
    def create_donation_detail(cls, need_type: NeedType, amount: int, donation: Donation, total_cost):
        try:
            return DonationDetail.objects.create(
                need_type=need_type,
                amount=amount,
                donation=donation,
                total_cost=total_cost
            )
        except Exception as e:
            raise ValidationError('Error while creating donation detail: {e}'.format(e=str(e)))
