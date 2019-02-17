from FDSops.settings import BASE_IMAGE_URL,IMAGE_SIZE

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
        try:
            self.__image = Image.open(BytesIO(response.content))
        except:
            raise FileNotFoundError("url地址错误")
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
            #缩小尺寸到box,找到中间位置
            region = self.__image.crop(box)
            #切图
            image2 = region.resize((IMAGE_SIZE[parameter][1]), Image.ANTIALIAS)
            return image2


        elif handle == "resize":
            image2 = self.__image.resize((IMAGE_SIZE[parameter][1]), Image.ANTIALIAS)
            return image2
        else:
            pass


    def clipimage(self):
        """
        处理图片，寻找中间位置
        :return:
        """
        width = int(self.size[0])
        height = int(self.size[1])
        if (width > height):
            dx = width - height
            box = (dx / 2, 0, height + dx / 2, height)
        else:
            dx = height - width
            box = (0, dx / 2, width, width + dx / 2)
        return box


