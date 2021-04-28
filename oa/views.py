import json

from django.utils.six import BytesIO
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import requests
import qrcode
import time
import hashlib

from oa.api import is_login, check_cookie, check_login, model_to_dict, check_stu_login, \
    check_stu_login_cookie, url_change, search_items, student_check, get_check_record_table, \
    items_to_table, update_item, search_stu_item, add_stu_to_item, generate_check_info, get_check_info_api
from django.views.decorators.clickjacking import xframe_options_sameorigin


@csrf_exempt
def login(request):
    dt = dict()
    if request.POST:
        info = request.POST
        print(info)
        dt['email'] = info.get('email')
        dt['password'] = info.get('password')
        m = hashlib.sha1()
        m.update(dt['password'].encode(encoding="utf-8"))
        m.hexdigest()
        dt['password'] = m.hexdigest()
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
    if not flag:
        return render(request, 'login.html')
    rank = model_to_dict(rank)
    print(json.dumps(rank))
    return render(request, 'teacher.html', rank)


@xframe_options_sameorigin
def check(request):
    flag, rank = check_cookie(request)
    if not flag:
        return render(request, 'login.html', {'error_msg': ''})
    uid = model_to_dict(rank).get('uid')
    keys = request.GET.keys()
    dt = dict()
    for key in keys:
        dt[key] = request.GET[key]
    print(dt)
    dt['uid'] = uid
    dt['time'] = round(time.time())
    # 生成签到记录
    dt['check_id'] = generate_check_info(t_uid=uid, check_time=dt['time'], item_id=dt['class_list'])
    if not dt.get('N'):
        dt['N'] = 181.0
    if not dt.get('E'):
        dt['E'] = 181.0
    print(dt)
    return render(request, 'check.html', dt)


def get_check_info(request):
    check_id = request.GET.get('check_id')
    res = get_check_info_api(check_id)
    res = json.dumps(res)
    return HttpResponse(res)


def logout(request):
    req = redirect('/login/')
    req.delete_cookie('email')
    req.delete_cookie('password')
    return req


def make_qrcode(request):
    print(request)
    print(111)
    dt = request.GET.dict()
    url = f"http://192.168.100.143:8000/stuIndex/?"
    url = url_change(url, dt)
    print(f'qrcode:{url}')
    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image()
    buf = BytesIO()
    img.save(buf)
    img_stream = buf.getvalue()
    response = HttpResponse(img_stream, content_type="image/jpg")
    return response


def stu_login(request):
    dt = dict()
    if request.POST:
        info = request.POST
        dt['uid'] = info.get('uid')
        dt['password'] = info.get('password')
        # TODO：password 加密
        if check_stu_login(dt['uid'], dt['password']) == 0:
            # return render(request, 'teacher.html', dt)
            response = redirect('/stuIndex/')
            response.set_cookie('uid', dt['uid'], 7200)
            response.set_cookie('password', dt['password'], 7200)
            return response
        else:
            if check_stu_login(dt['uid'], dt['password']) == 2:
                dt['error_msg'] = '学号错误'
            else:
                dt['error_msg'] = '密码错误'
            return render(request, 'stu_login.html', dt)
    else:
        flag, rank = check_stu_login_cookie(request)
        if flag:
            return redirect('/stuIndex/')
        return render(request, 'stu_login.html', {'error_msg': ''})


def stu_index(request):
    # 如果当前时间和二维码的时间差距超过15s就当过期处理
    flag, rank = check_stu_login_cookie(request)
    if not flag:
        return render(request, 'stu_login.html')
    print(request)
    if not request.GET.get('time'):
        return render(request, 'stu_index.html')
    rank = model_to_dict(rank)
    check_time = int(request.GET.get('time'))
    t = time.time()
    t = int(round(t * 1000))
    print(f't:{t}, check_time:{check_time}')
    if t - check_time > 15 * 1000:
        return render(request, 'stu_index.html', {'res_msg': '二维码已过期'})
    res = student_check(rank['uid'], request.GET.get('cls_id'), request.GET.get('check_id'))
    return render(request, 'stu_index.html', {'res_msg': res})


@xframe_options_sameorigin
def check_setting(request):
    dt = dict()
    print(request.GET)
    items = search_items(request.GET['uid'])
    dt['class_list'] = items
    print(dt)
    return render(request, 'check_setting.html', dt)


@xframe_options_sameorigin
def check_history(request):
    return render(request, 'check_history.html')


def get_record_table(request):
    flag, rank = check_cookie(request)
    if not flag:
        return render(request, 'login.html', {'error_msg': ''})
    uid = model_to_dict(rank).get('uid')
    total, table = get_check_record_table(uid, page=int(request.GET.get('page'))-1, limit=int(request.GET.get('limit')))
    # test_data = {"check_id": 1, "check_item": "计算机171", "check_time": "2021/4/17/15:30", "checked_count": 20,
    #              "total_count": 21, "unchecked_stu": ['石头人']}
    # table.append(test_data)
    res = {"code": 0, "msg": "", "count": total, "data": table}
    res = json.dumps(res)
    return HttpResponse(res)


def add_item(request):
    flag, rank = check_cookie(request)
    if not flag:
        return render(request, 'login.html', {'error_msg': ''})
    uid = model_to_dict(rank).get('uid')
    if request.POST:
        print(request.POST)
        update_item(uid, request.POST.get('name'), 0)
    return render(request, 'search_item.html')


def get_items(request):
    flag, rank = check_cookie(request)
    if not flag:
        return render(request, 'login.html', {'error_msg': ''})
    uid = model_to_dict(rank).get('uid')
    items = search_items(uid)
    items = items_to_table(items)
    res = {"code": 0, "msg": "", "count": len(items), "data": items}
    res = json.dumps(res)
    return HttpResponse(res)


@xframe_options_sameorigin
def search_item(request):
    return render(request, 'search_item.html')


def change_stu_item(request):
    flag, rank = check_cookie(request)
    if not flag:
        return render(request, 'login.html', {'error_msg': ''})
    uid = model_to_dict(rank).get('uid')
    if request.POST:
        print(1)
        # update_item(uid, request.POST.get('name'), 2, uid=request.POST.get('uid'))
    return render(request, 'search_item.html')


def del_item(request):
    flag, rank = check_cookie(request)
    if not flag:
        return render(request, 'login.html', {'error_msg': ''})
    uid = model_to_dict(rank).get('uid')
    if request.POST:
        update_item(uid, request.POST.get('name'), 1, request.POST.get('uid'))
    return render(request, 'search_item.html')


@xframe_options_sameorigin
def add_stu(request):
    flag, rank = check_cookie(request)
    if not flag:
        return render(request, 'login.html', {'error_msg': ''})
    dt = dict()

    if request.POST:
        dt['itemId'] = request.GET.get('itemId')
        print(request.POST)
        add_stu_to_item(dt['itemId'], request.POST.get('uid'))
    return render(request, 'add_stu.html', dt)


@xframe_options_sameorigin
def search_stu(request):
    flag, rank = check_cookie(request)
    if not flag:
        return render(request, 'login.html', {'error_msg': ''})
    dt = dict()
    dt['itemId'] = request.GET.get('itemId')
    return render(request, 'add_stu.html', dt)


def get_stu_item(request):
    flag, rank = check_cookie(request)
    if not flag:
        return render(request, 'login.html', {'error_msg': ''})
    dt = search_stu_item(request.GET.get('itemId'))
    res = {"code": 0, "msg": "", "count": len(dt), "data": dt}
    res = json.dumps(res)
    return HttpResponse(res)


def test(request):
    return render(request, 'test.html')


@xframe_options_sameorigin
def index(request):
    return render(request, 'index.html')

