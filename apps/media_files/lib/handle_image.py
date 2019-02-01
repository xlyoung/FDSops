from FDSops.settings import FDFS_URL ,BASE_IMAGE_URL,IMAGE_SIZE

import requests
from PIL import Image
from io import BytesIO


class HandleImage():
    """
    图片处理
    """
    def __init__(self,url=None):
        if url is None:
            url = BASE_IMAGE_URL
        self.url = url
        response = requests.get(self.url)
        self.__image = Image.open(BytesIO(response.content))
        self.size = self.__image.size



    def himage(self,parameter):
        """
        :param url: 获取fastdfs的url地址
        :param parameter: 指定操作参数
        :return:返回图片
        """
        #获取执行参数
        handle = IMAGE_SIZE[parameter][0]
        if handle == "crop":
            print(self.size)
            box = self.clipimage()

            pass
        elif handle == "resize":
            image2 = self.__image.resize((IMAGE_SIZE[parameter][1]), Image.ANTIALIAS)
            image2.show()
            print (self.size)
            return image2
            pass
        else:
            pass


    def clipimage(self):
        width = int(self.size[0])
        height = int(self.size[1])
        box = ()
        if (width > height):
            dx = width - height
            box = (dx / 2, 0, height + dx / 2, height)
        else:
            dx = height - width
            box = (0, dx / 2, width, width + dx / 2)
        return box