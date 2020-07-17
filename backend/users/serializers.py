from django.contrib.auth import get_user_model
from rest_auth.models import TokenModel
from rest_framework import serializers

User = get_user_model()


class UserShortSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'full_name')

    def get_full_name(self, user):
        return "{first_name} {last_name}".format(
            first_name=user.first_name,
            last_name=user.last_name
        )


class TokenSerializer(serializers.ModelSerializer):
    """
    Serializer for Token model.
    """

    token = serializers.CharField(source='key')

    user = UserShortSerializer()

    class Meta:
        model = TokenModel
        fields = ('token', 'user')
