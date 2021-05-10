# -*- coding: utf-8 -*-
from functools import wraps

from django.shortcuts import render

from oa.models import Teacher, Student, Item, CheckInfo, StuItem, CheckRecord
from datetime import date, datetime
import time


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
# @params check_id 签到id
# @result record_id 学生签到记录
# @result check_time 时间戳
# @return res  签到信息成功，重复，不在名单等
def student_check(stu_id, cls_id, check_id, check_type=1, check_reason=""):
    print(f'stu_id:{stu_id}, cls_id:{cls_id}, check_id:{check_id}')
    # 检查是否在名单内
    if not stu_in_cls(stu_id, cls_id):
        result_info = '抱歉，不在本次签到名单中'
    # 检查是否签到过
    elif is_checked(stu_id, check_id):
        result_info = '您已签到过，请勿重复签到'
    # 增加一条签到记录，修改签到信息中已签到的人数
    else:
        CheckRecord.objects.create(check_id=check_id, uid=stu_id, check_time=int(round(time.time())),
                                   check_type=check_type, check_reason=check_reason)
        count = int(CheckInfo.objects.get(check_id=check_id).checked_count)
        CheckInfo.objects.filter(check_id=check_id).update(checked_count=count + 1)
        result_info = '签到成功'
    return result_info


# 检查是否在名单内
def stu_in_cls(stu_id, cls_id):
    if not len(StuItem.objects.filter(stu_id=stu_id, item_id=cls_id)):
        return False
    return True


# 检查是否签到过
def is_checked(stu_id, check_id):
    if len(CheckRecord.objects.filter(uid=stu_id, check_id=check_id)):
        return True
    return False


# 查询教师的所有名单
# @params t_uid 教师编号
# @return items 名单对象
def search_items(t_uid):
    items = Item.objects.filter(t_uid=t_uid)
    item_dict = []
    for item in items:
        item_dict.append(model_to_dict(item))
    return item_dict


def get_check_record_table(uid, page, limit):
    # @params uid 教师id
    # @return check_id 签到记录id
    # @return total_count 签到人数
    # @return checked_count 实际签到人数
    # @return check_time  签到时间
    # @return item  签到名单
    # @return unchecked_name_list 未签到人名字
    # 获取uid所有check_info
    total, res = get_all_check_info(uid, page, limit)
    # 将item_id转为名单名称
    res = item_id_to_name(res)
    # 未签到的人 = item的人 - check_record找check_id签到的人
    res = find_unchecked_name_list(res)
    return total, res


# 获取uid所有check_info
def get_all_check_info(uid, page=-1, limit=-1):
    info_array = CheckInfo.objects.filter(t_uid=uid)
    total = len(info_array)
    if page != -1:
        info_array = CheckInfo.objects.filter(t_uid=uid)[page*limit:page*limit+limit]
    res = []
    for info in info_array:
        res.append(model_to_dict(info))
    if len(res):
        print(f"res[0]：{res[0]}")
    return total, res


# 将item_id转为名单名称
def item_id_to_name(objs):
    for obj in objs:
        obj['item_name'] = Item.objects.get(uid=obj['item_id']).name
    return objs


# 未签到的人 = item的人 - check_record找check_id签到的人
def find_unchecked_name_list(objs):
    for obj in objs:
        s = set()
        stu_list = CheckRecord.objects.filter(check_id=obj['check_id'])
        for stu in stu_list:
            s.add(stu.uid)
        res_s = set()
        stu_item = StuItem.objects.filter(item_id=obj['item_id'])
        for stu in stu_item:
            res_s.add(stu.stu_id)
        for stu in s:
            res_s.remove(stu)
        obj['unchecked_stu'] = []
        for stu_id in res_s:
            obj['unchecked_stu'].append(Student.objects.get(uid=stu_id).name)
    return objs


# 处理名单显示
def items_to_table(items):
    for item in items:
        item['stu'] = StuItem.objects.filter(item_id=item['uid']).count()
    return items


# 改变名单 0:add, 1:delete, 2:update TODO
def update_item(t_uid, name, op, uid=-1):
    if uid == -1:
        Item.objects.create(name=name, t_uid=t_uid)
    elif op == 1:
        Item.objects.filter(uid=uid).delete()
        StuItem.objects.filter(item_id=uid).delete()
        return
    else:
        return


def search_stu_item(item_id):
    stu_ids = StuItem.objects.filter(item_id=item_id)
    stus = []
    for stu_item in stu_ids:
        obj = dict()
        obj['uid'] = stu_item.stu_id
        obj['name'] = Student.objects.get(uid=int(stu_item.stu_id)).name
        stus.append(obj)
    return stus


def add_stu_to_item(item_id, stu_id):
    StuItem.objects.create(item_id=item_id, stu_id=stu_id)


# 生成签到记录
# @params t_uid 教师id
# @params check_time 发起时间
# @params item_id 名单id
# @return check_id 签到的id

def generate_check_info(t_uid, check_time, item_id):
    print(f't_uid:{t_uid}, check_time:{check_time}, item_id:{item_id}')
    obj = CheckInfo.objects.create(t_uid=t_uid, check_time=check_time, item_id=item_id,
                                   checked_count=0, total_count=int(StuItem.objects.filter(item_id=item_id).count()))
    return obj.check_id


def get_check_info_api(check_id):
    r = CheckInfo.objects.get(check_id=check_id)
    res = dict()
    res['checked_count'] = r.checked_count
    res['total'] = r.total_count
    res['item_id'] = r.item_id
    print(res)
    return res
