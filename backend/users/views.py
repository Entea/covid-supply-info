from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import ugettext_lazy as _

from users.services import TokenService


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request, *args, **kwargs):
        return self.logout(request)

    def logout(self, request):
        TokenService.logout(user=request.user)

        response = Response({"detail": _("Successfully logged out.")},
                            status=status.HTTP_200_OK)
        return response
