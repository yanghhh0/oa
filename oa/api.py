# -*- coding: utf-8 -*-
from functools import wraps

from django.shortcuts import render

from oa.models import Teacher, Student
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


def check_stu_login_cookie(request):
    d = request.COOKIES.keys()
    print(d)
    if "uid" in d and "password" in d:
        uid = request.COOKIES['uid']
        password = request.COOKIES['password']
        print(f"{uid}, {password}")
        select_user = Student.objects.filter(uid=uid).filter(password=password)
        if len(select_user) == 0:
            return False, -1
        else:
            return True, select_user[0]
    else:
        return False, -1


def check_stu_login(uid, password):
    if len(Student.objects.filter(uid=uid)) > 0:
        if len(Student.objects.filter(password=password)):
            return 0  # 成功
        else:
            return 1  # 密码错误
    else:

        return 2  # 学号错误


def url_change(url, params):
    flag = False
    for key, value in params.items():
        if flag:
            url += f'&{key}={value}'
        else:
            url += f'{key}={value}'
            flag = True
    return url


# 学生签到
# @params stu_id 学号
# @params cls_id 名单编号
# @params record_id 签到记录id
def student_check(stu_id, cls_id, record_id):
