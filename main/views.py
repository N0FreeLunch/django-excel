from django.shortcuts import render, redirect
from random import *
from .models import *
from sendEmail.views import *

# Create your views here.
def index(request):
    return render(request, 'main/index.html')

def signup(request):
    return render(request, 'main/signup.html')

def join(request):
    print(request)
    name = request.POST["signupName"]
    email = request.POST["signupEmail"]
    pw = request.POST["signupPW"]
    user = User(user_name = name, user_email = email, user_password = pw)
    user.save()
    code = randint(1000,9999)
    response = redirect('main_verifyCode')
    response.set_cookie('code', code)
    response.set_cookie('user_id',user.id)
    send_result = send(email,code)
    if send_result:
        return response
    else:
        return HttpResponse("이메일 발송을 실패했습니다.")
    # return response
    # return redirect('main_verifyCode')

def signin(requset):
    return render(requset, 'main/signin.html')

def verifyCode(request):
    return render(request, 'main/verifyCode.html')

def verify(request):
    user_code = request.POST["verifyCode"]
    cookie_code = request.COOKIES.get('code')
    if user_code == cookie_code:
        user = User.objects.get(id = request.COOKIES.get('user_id'))
        user.user_validate = 1
        user.save()
        response = redirect('main_index')
        response.delete_cookie('code')
        response.delete_cookie('user_id')
        response.set_cookie('user',user)
        return response
    else:
        return redirect('main_verifyCode')

def result(request):
    return render(request, 'main/result.html')
