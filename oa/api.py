# -*- coding: utf-8 -*-
from functools import wraps

from django.shortcuts import render

from oa.models import Teacher
from datetime import date, time, datetime


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


def model_to_dict(model_obj):
    """
    将一个model对象转换成字典
    """
    att_dict = {}
    for field in model_obj._meta.fields:
        name = field.attname  # 获取字段名
        value = getattr(model_obj, name)  # 获取对象属性
        att_dict[name] = value  # 生成字典
    return att_dict



