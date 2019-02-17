import time
import hashlib
from rest_framework import exceptions

def md5(user):
    """
    自定义生成md5tocken值
    :param： user:
    :return: md5_token值
    """
    try:
        ctime = str(time.time())
        m = hashlib.md5(bytes(str(user), encoding='utf-8'))
        m.update(bytes(ctime, encoding='utf-8'))
        return m.hexdigest()
    except Exception as e:
        raise exceptions.ValidationError("md5token值获取失败")