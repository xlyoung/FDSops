# Create your views here.
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets , status
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import permissions
from rest_framework import authentication
from rest_framework import mixins
from rest_framework.authtoken.views import ObtainAuthToken

from random import choice

from .serializers import EmailSerializers, UserRegSerializer, UserDetailSerializer
from .models import EmailVerifyCode,UserToken
from  utils.email import SendMail
from .lib.md5_token import md5
from utils.auth import TokenAuthtication
from rest_framework.versioning import URLPathVersioning





#获取用户模块
User = get_user_model()




class CustomBackend(ModelBackend,):
    """
    定义用户登陆验证
    """

    def authenticate(self, username=None, password=None, **kwargs):

        try:
            user = User.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                #为用户创建token
                token = md5(user)
                #存在就更新，不存在就创建
                UserToken.objects.update_or_create(user=user,defaults={'token':token})
                return user
        except Exception as e:

            return None

class CustomAuthToken(ObtainAuthToken):
    """
    token获取接口
    """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        return Response({
            # 'user':user,
            'user_id': user.pk,
            'token': user.usertoken.token,
            'email': user.email,
        })

class EmailCodeViewset(CreateModelMixin,viewsets.GenericViewSet):
    """
    发送短信验证码
    """

    #版本控制
    versioning_class = URLPathVersioning
    serializer_class = EmailSerializers


    def generate_code(self):
        """
        生成4位数字验证码
        :return:
        """
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))
        return "".join(random_str)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]


        code = self.generate_code()

        send_to_email = SendMail(code=code,email=email)

        email_status = send_to_email.sendmail()

        print (email_status)
        if email_status != 0:
            return Response({
                "email":email_status
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = EmailVerifyCode(code=code, email=email)
            code_record.save()
            return Response({
                "email":email

            }, status=status.HTTP_201_CREATED)


class UserViewset(CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    用户
    """
    #版本控制
    versioning_class = URLPathVersioning
    serializer_class = UserRegSerializer
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializer

        return UserDetailSerializer

    permission_classes = (permissions.IsAuthenticated, )
    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []

        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        re_dict = serializer.data
        token = md5(user)
        re_dict["token"] = token
        re_dict["name"] = user.name if user.name else user.username
        UserToken.objects.update_or_create(user=user,defaults={'token':token})

        return Response(re_dict, status=status.HTTP_201_CREATED)

    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()

