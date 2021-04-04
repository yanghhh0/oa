import json

from django.utils.six import BytesIO
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

import qrcode
import time
from api import is_login, check_cookie, check_login, model_to_dict
from django.views.decorators.clickjacking import xframe_options_sameorigin

HOST = '127.0.0.1?'


@csrf_exempt
def login(request):
    dt = dict()
    if request.POST:
        info = request.POST
        print(info)
        dt['email'] = info.get('email')
        dt['password'] = info.get('password')
        # TODO：password 加密
        if check_login(dt['email'], dt['password']) == 0:
            # return render(request, 'teacher.html', dt)
            response = redirect('/teacher/')
            response.set_cookie('email', dt['email'], 7200)
            response.set_cookie('password', dt['password'], 7200)
            return response
        else:
            if check_login(dt['email'], dt['password']) == 2:
                dt['error_msg'] = '邮箱错误'
            else:
                dt['error_msg'] = '密码错误'
            return render(request, 'login.html', dt)
    else:
        flag, rank = check_cookie(request)
        if flag:
            return redirect('/teacher/')
        return render(request, 'login.html', {'error_msg': ''})


@csrf_exempt
def register(request):
    dt = dict()
    if request.POST:
        dt['email'] = request.POST['email']
        dt['password'] = request.POST['password']
        return render(request, 'login.html', dt)
    else:
        return render(request, 'register.html')


def teacher(request):
    flag, rank = check_cookie(request)
    rank = model_to_dict(rank)
    print(json.dumps(rank))
    return render(request, 'teacher.html', rank)


@xframe_options_sameorigin
def notice(request):
    return render(request, 'notice.html')


@xframe_options_sameorigin
def manage(request):
    return render(request, 'manage.html')


@xframe_options_sameorigin
def data(request):
    return render(request, 'data.html')


@xframe_options_sameorigin
def check(request):
    return render(request, 'check.html')


def logout(request):
    req = redirect('/login/')
    req.delete_cookie('email')
    req.delete_cookie('password')
    return req


def make_qrcode(request):
    tm = int(time.time())
    url = HOST + "time=%s" % tm
    img = qrcode.make(url)
    buf = BytesIO()
    img.save(buf)
    img_stream = buf.getvalue()
    response = HttpResponse(img_stream, content_type="image/jpg")
    return response
