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

    def thumbnails(self,url,handle):
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))
        image2 = image.resize((IMAGE_SIZE[handle]))
        return image2