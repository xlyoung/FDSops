from django.core.mail import send_mail


class SendMail(object):
    """
    邮件发送
    """


    def __init__(self,code,email):
        self.send_title = "Hi, Welcome to Register  Fdsops Account!"
        self.send_message = "your conde is %s ,Please take care of it." % code
        self.send_obj_list = [email]
        self.send_html_message = '<h1>包含 html 标签且不希望被转义的内容</h1>'



    def sendmail(self,code,email):
        status = send_mail(
            self.send_title,
            "your conde is %s ,Please take care of it." % code,
            None,
            self.send_obj_list,
            self.send_html_message
        )
        if status:
            return 0
        else:
            return -1
