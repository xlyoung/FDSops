__author__ = 'young'


import requests
import json
from FDSops.settings import API_KEY



class YunPian(object):

    def __init__(self,api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_sms(self,code,mobile):
       parmas:{
           "apikey": self.api_key,
           "mobile": mobile,
           "text" : "[test]"
       }
       response = requests.post(self.single_send_url,data=parmas)
       re_dict = json.load(response.text)

       print (re_dict)

if __name__ == "__main__":
    yun_pian = YunPian(API_KEY)
    yun_pian.send_sms("2017","13726251800")