from rest_auth.models import TokenModel
from rest_framework import serializers


class TokenSerializer(serializers.ModelSerializer):
    """
    Serializer for Token model.
    """

    token = serializers.CharField(source='key')

    class Meta:
        model = TokenModel
        fields = ('token',)
