from django.utils.six import BytesIO
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from oa.service import dataHelper
import json
import qrcode
import time

HOST = '127.0.0.1?'


def login(request):
    dt = dict()
    if request.POST:
        info = request.POST
        print(info)
        dt['email'] = info.get('email')
        dt['password'] = info.get('password')
        # TODO：password 加密
        if dataHelper.check_login(dt['email'], dt['password']) == 0:
            return render(request, 'teacher.html', dt)
        else:
            if dataHelper.check_login(dt['email'], dt['password']) == 2:
                dt['error_msg'] = '邮箱错误'
            else:
                dt['error_msg'] = '密码错误'
            return render(request, 'login.html', dt)
    return render(request, 'login.html', dt)


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
    return render(request, 'teacher.html')


def notice(request):
    return render(request, 'notice.html')


def manage(request):
    return render(request, 'manage.html')


def data(request):
    return render(request, 'data.html')


def check(request):

    return render(request, 'check.html')


def make_qrcode(request):
    tm = int(time.time())
    url = HOST + f"time={tm}"
    img = qrcode.make(url)
    buf = BytesIO()
    img.save(buf)
    img_stream = buf.getvalue()
    response = HttpResponse(img_stream, content_type="image/jpg")
    return response
