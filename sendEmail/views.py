from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string

import os, json
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
secret_file = os.path.join(BASE_DIR, 'secret.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    """비밀 변수를 가져오거나 명시적 예외를 반환한다."""
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

# Create your views here.
def send(receiverEmail, verifyCode):
    try:
        content = {'verifyCode':verifyCode}
        msg_html = render_to_string('sendEmail/email_format.html',content)
        msg = EmailMessage(subject="인증코드 발송 메일",body=msg_html,from_email=get_secret("MAIL"),bcc=[receiverEmail])
        msg.content_subtype='html'
        msg.send()
        return True
    except:
        return False
    # return HttpResponse("sendEmail, send function!")
