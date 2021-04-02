# -*- coding: utf-8 -*-


from oa.models import Teacher


def check_login(email, password):
    if len(Teacher.objects.filter(email=email)) > 0:
        if len(Teacher.objects.filter(password=password)):
            return 0  # 成功
        else:
            return 1  # 密码错误
    else:
        return 2  # 邮箱错误


