# -*- coding: utf-8 -*-
from functools import wraps

from django.shortcuts import render

from oa.models import Teacher


def check_login(email, password):
    if len(Teacher.objects.filter(email=email)) > 0:
        if len(Teacher.objects.filter(password=password)):
            return 0  # 成功
        else:
            return 1  # 密码错误
    else:
        return 2  # 邮箱错误


def check_cookie(request):
    d = request.COOKIES.keys()
    if "email" in d and "password" in d:
        email = request.COOKIES['email']
        password = request.COOKIES['password']
        select_user = Teacher.objects.filter(email=email).filter(password=password)
        if len(select_user) == 0:
            return False, -1
        else:
            return True, select_user[0]
    else:
        return False, -1


def is_login(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        (flag, rank) = check_cookie(request)
        if flag:
            return func(request, *args, **kwargs)
        else:
            return render(request, 'login.html', {'error_msg': ''})
    return inner




