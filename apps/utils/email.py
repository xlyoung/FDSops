from django.core.mail import send_mail
from FDSops.settings import EMAIL_HOST_USER

class SendMail(object):
    """
    邮件发送
    """


    def __init__(self,code,email):
        self.send_title = "Hi, Welcome to Register  Fdsops Account!"
        self.send_message = "your conde is %s ,Please take care of it." % code
        self.send_obj_list = [email]
        self.from_email_add = EMAIL_HOST_USER
        self.send_html_message = '<h1>包含 html 标签且不希望被转义的内容</h1>'



    def sendmail(self):
        try:
            status = send_mail(
                self.send_title,
                self.send_message,
                self.from_email_add,
                self.send_obj_list,
                fail_silently=False
            )
        except Exception as e:
            print (e)
            return -1

        if status:
            return 0
        else:
            return -1
