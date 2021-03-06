from django.shortcuts import render, redirect
from random import *
from .models import *
from sendEmail.views import *
import hashlib

# Create your views here.
def index(request):
    # print(type(request.session))
    # print((request.session.__dict__))
    print(type(request.session.keys()))
    for value in request.session.keys():
        print(value)

    # print(request.session["user_name"])
    # print(request.session["user_email"])
    if 'user_name' in request.session.keys():
        return render(request, 'main/index.html')
    else:
        return redirect('main_signin')

def signup(request):
    for value in request.session.keys():
        print(value)
    return render(request, 'main/signup.html')

def join(request):
    for value in request.session.keys():
        print(value)
    print(request)
    name = request.POST["signupName"]
    email = request.POST["signupEmail"]
    pw = request.POST["signupPW"]
    # print("join")
    # print(pw)
    encoded_pw = pw.encode()
    # print(encoded_pw)
    encrypted_pw = hashlib.sha256(encoded_pw).hexdigest()
    user = User(user_name = name, user_email = email, user_password = encrypted_pw)
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

def signin(request):
    for value in request.session.keys():
        print(value)
    return render(request, 'main/signin.html')

def login(request):
    for value in request.session.keys():
        print(value)
    loginEmail = request.POST['loginEmail']
    loginPW = request.POST['loginPW']

    try:
        user = User.objects.get(user_email = loginEmail)
    except Exception as e:
        return redirect('main_loginFail')

    encoded_loginPW = loginPW.encode()
    encrypted_pw = hashlib.sha256(encoded_loginPW).hexdigest()

    if user.user_password == encrypted_pw:
        print("login")
        request.session['user_name'] = user.user_name
        request.session['user_email'] = user.user_email
        request.session['test'] = "test"
        return redirect('main_index')
    else:
        return redirect('main_loginFail')

def loginFail(request):
    return render(request, 'main/loginFail.html')

def logout(request):
    for value in request.session.keys():
        print(value)
    del request.session['user_name']
    del request.session['user_email']
    return redirect("main_signin")

def verifyCode(request):
    for value in request.session.keys():
        print(value)
    return render(request, 'main/verifyCode.html')

def verify(request):
    for value in request.session.keys():
        print(value)
    user_code = request.POST["verifyCode"]
    cookie_code = request.COOKIES.get('code')
    if user_code == cookie_code:
        user = User.objects.get(id = request.COOKIES.get('user_id'))
        user.user_validate = 1
        user.save()
        response = redirect('main_index')
        response.delete_cookie('code')
        response.delete_cookie('user_id')
        # response.set_cookie('user',user)
        request.session['user_name'] = user.user_name
        request.session['user_email'] = user.user_email
        return response
    else:
        return redirect('main_verifyCode')

def result(request):
    for value in request.session.keys():
        print(value)
    # print(request.session.__dict__)
    # print(request.session.keys())
    if 'user_name' in request.session.keys():
        content = {}
        content['grade_calculate_dic'] = request.session['grade_calculate_dic']
        content['email_domain_dic'] = request.session['email_domain_dic']
        del request.session['grade_calculate_dic']
        del request.session['email_domain_dic']
        print(content)
        return render(request, 'main/result.html', content)
    else:
        return redirect('main_signin')
