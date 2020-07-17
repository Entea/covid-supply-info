from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import NotFound, ValidationError

User = get_user_model()


class TokenService:
    model = Token

    @classmethod
    def get(cls, **filters):
        try:
            return cls.model.objects.get(**filters)
        except cls.model.DoesNotExist:
            raise NotFound('Token not found')

    @classmethod
    def logout(cls, user: User):

        token = cls.get(user=user)

        try:
            token.delete()
        except IntegrityError:
            raise ValidationError('Can not logout')
