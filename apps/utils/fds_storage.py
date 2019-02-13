from django.core.files.storage import Storage
from django.conf import settings
from django.utils.deconstruct import deconstructible
from fdfs_client.client import *



@deconstructible
class FDFSStorage(Storage):
    '''fast dfs文件存储类'''
    def __init__(self, client_conf=None, base_url=None):
        '''初始化'''
        if client_conf is None:
            client_conf = settings.FDFS_CLIENT_CONF

        self.client_conf = client_conf

        if base_url is None:
            base_url = settings.FDFS_URL

        self.base_url = base_url


    def _open(self, name, mode='rb'):

        # #读取fds配置文件
        # client_conf_obj = get_tracker_conf(self.client_conf)
        # # 创建一个Fdfs_client对象
        #
        # client = Fdfs_client(client_conf_obj)
        #
        # return client.get_meta_data(name,mode)
        pass


    def _save(self, name, content):
        '''保存文件时使用'''
        # name:你选择上传文件的名字 test.jpg
        # content:包含你上传文件内容的File对象

        #读取fds配置文件
        client_conf_obj = get_tracker_conf(self.client_conf)
        # 创建一个Fdfs_client对象

        client = Fdfs_client(client_conf_obj)

        # 上传文件到fast dfs系统中
        res = client.upload_by_buffer(content.read())


        # dict
        # {
        #     'Group name': group_name,
        #     'Remote file_id': remote_file_id,
        #     'Status': 'Upload successed.',
        #     'Local file name': '',
        #     'Uploaded size': upload_size,
        #     'Storage IP': storage_ip
        # }
        if res.get('Status') != 'Upload successed.':
            # 上传失败
            raise Exception('上传文件到fast dfs失败')

        # 获取返回的文件ID
        filename = res.get('Remote file_id')
        return filename

    def exists(self, name):
        '''Django判断文件名是否可用,返回False表示一直可用'''
        return False

    def url(self, name):
        '''返回访问文件的url路径,就是ImageField字段image的url属性的值,image.url,默认的image的url是这样的格式：'/media/001.jpg' '''
        return self.base_url + name