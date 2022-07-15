from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions


token_duration = 7  # in days


class CustomTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        from datetime import timedelta, datetime

        today = datetime.now()
        response = super().authenticate(request)
        if response is not None:
            if response[1].created + timedelta(days=token_duration) > today:
                raise exceptions.AuthenticationFailed(_("Token is expired"))
        return response
