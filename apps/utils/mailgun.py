from django.core.mail import EmailMultiAlternatives
from anymail.message import attach_inline_image_file
from FDSops.settings import SENDEMAIL


import requests
import json

class SendEmailMailGun(object):

    def send_email(self,code,email):
        email_list = []
        msg = EmailMultiAlternatives(
            subject="Hi,%s please verify your Fdsops account!",
            body = "your conde is %s ,Please take care of it." %code,
            from_email=SENDEMAIL,
            to=[email],
            reply_to=["Helpdesk <support@example.com>"],
        )
        logo_cid = attach_inline_image_file(msg, "/Users/yangzhuohua/python/workspace/FDSops/media/130G6121429-0.jpg")
        html = """<img alt="Logo" src="cid:{logo_cid}">
          <p>Please <a href="http://example.com/activate">activate</a>
          your account</p>""".format(logo_cid=logo_cid)

        msg.attach_alternative(html, "text/html")

        # # Optional Anymail extensions:
        msg.metadata = {"user_id": "8675309", "experiment_variation": 1}
        msg.tags = ["activation", "onboarding"]
        msg.track_clicks = True

        # Send it:
        msg.send()
        if msg.anymail_status.status.issubset({'queued', 'sent'}):
            return 0
        else :
            raise ConnectionError("发送邮件失败")
            return 1