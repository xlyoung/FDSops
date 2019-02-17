
from users import models
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from datetime import datetime,timedelta
from FDSops.settings import EXPIRING_TOKEN_DAYS



class TokenAuthtication(BaseAuthentication):
    """
    token认证
    """
    def authenticate(self, request):
        token = request._request.GET.get('token')
        token_obj = models.UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed('用户认证失败')
        now = datetime.now()
        if token_obj.add_time < now - timedelta(days=int(EXPIRING_TOKEN_DAYS)):
            raise exceptions.AuthenticationFailed('Token已过期')
        return (token_obj.user,token_obj)

    def authenticate_header(self, request):
        pass
