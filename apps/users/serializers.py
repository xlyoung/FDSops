__author__ = 'young'


from rest_framework import serializers
from django.contrib.auth import get_user_model

from FDSops.settings import REGEX_MOBILE,REGEX_EMAIL
from .models import EmailVerifyCode
import re
from datetime import datetime ,timedelta
from rest_framework.validators import UniqueValidator




User = get_user_model()


class EmailSerializers(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        """
        验证手机号码

        :param attrs:
        :return:
        """
        #邮箱是否注册
        if User.objects.filter(email=email).count():
            raise serializers.ValidationError("用户已存在")

        #验证邮箱是否合法
        if not re.match(REGEX_EMAIL,email):
            raise serializers.ValidationError("邮箱地址非法")

        #验证发送频率
        one_mintes_ago = datetime.now() - timedelta(hours=0,minutes=1,seconds=0)
        if EmailVerifyCode.objects.filter(add_time__gt=one_mintes_ago,email=email):
            raise serializers.ValidationError("请在一分钟后再发送")


        return email

class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化类
    """
    class Meta:
        model = User
        fields = ("name", "gender", "birthday", "email", "mobile")

class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4,label="邮件验证码",
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "required": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 },
                                 help_text="验证码")
    username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])
    password = serializers.CharField(
        style={'input_type': 'password'},help_text="密码", label="密码", write_only=True,
    )

    email = serializers.EmailField(label="邮箱地址",help_text="邮箱地址",
                                   validators=[UniqueValidator(queryset=User.objects.all(),message="该邮箱已注册")]
    )

    def validate_code(self, code):
        """
        验证注册码
        :param code:
        :return:
        """
        verify_records = EmailVerifyCode.objects.filter(email=self.initial_data["email"]).order_by("-add_time")
        if verify_records:
            last_record = verify_records[0]
            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_mintes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")
            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        del attrs["code"]
        return attrs

    def create(self, validated_data):
        user = User(
            username = validated_data['username'],
            email = validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


    class Meta:
        model = User
        fields = ("username", "code", "email", "password")





