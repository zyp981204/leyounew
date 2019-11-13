from django.http import HttpResponse, response, JsonResponse
from django.shortcuts import render, redirect
from datetime import datetime
import json
import uuid
from django.urls import reverse
from django.core.serializers import serialize
from django.db.models import Q
from . import models

from utils.status_code import status_codes
from utils.check_tel import *
from utils.token_tool import make_token
from utils.encryption_tool import *
from utils.self_Alipay import *
from com_leyou.settings import ying_yong_si_yao, zhi_fu_bao_gong_yao


# Create your views here.

def get_uorder(request):
    uorder = reverse('order:user_order')
    return redirect(uorder)


def get_uinfo(request, id):
    return HttpResponse('123' + str(id))

def update_upwd(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        utel=data['telephone']
        data['new_pwd'] = encryption(str(data['new_pwd']))
        new_upwd=data['new_pwd']
        affect_row = models.userlogin.objects.filter(telephone=utel).update(password=new_upwd)
        return JsonResponse(status_codes["update_success"])
    else:
        return HttpResponse('this is Get method')

def update_uinfo(request):
    if request.method == 'POST':
        data=json.loads(request.body)
        new_uinfo=data['new_uinfo']
        print(new_uinfo)
        utel=new_uinfo['telephone']
        users = models.userlogin.objects.filter(telephone=utel)
        uid=users[0].id
        print(uid)
        affect_rows1 = models.userinfo.objects.filter(uid_id=uid).update(name=new_uinfo['name'],email=new_uinfo['email'])
        affect_rows2 = models.identification.objects.filter(user_id=uid).update(identification_num=new_uinfo['identification_num'],identification_type_id=new_uinfo['identification_type_id'],useful_date=new_uinfo['useful_date'],user_id=uid)
        affect_rows3 = models.emergency_contact.objects.filter(user_id=uid).update(contacts_name=new_uinfo['contacts_name'],contacts_num=new_uinfo['contacts_num'],user_id=uid)
        affect_rows4 = models.address.objects.filter(user_id=uid).update(address=new_uinfo['address'],user_id=uid)
        # affect_rows1.save()
        # affect_rows2.save()
        # affect_rows3.save()
        # affect_rows4.save()
        return JsonResponse(status_codes["update_success"])
    else:
        return HttpResponse('this is Get method')

# 手机号密码登录
def login(request):
    if request.method == 'POST':
        user = request.body
        data = json.loads(user)
        tel = data['telephone']
        password = data['password']
        # 查询手机号是否存在
        temp = list(models.userlogin.objects.filter(telephone=tel).values())
        print(temp)
        if(temp):
            get_pwd = temp[0]['password']
            pwd = data['password']
            # 比对密码是否相同
            flag =check_password(get_pwd,str(pwd))
            print(flag)
            if(flag):
                username = models.userlogin.objects.filter(telephone=tel).values('userinfo__name').first()
                name = username["userinfo__name"]
                # 构建令牌
                token = make_token(pwd)
                tel = temp[0]['telephone']
                status_codes["login_success"]["token"] = token.decode()
                status_codes["login_success"]["name"] = name
                status_codes["login_success"]["telephone"] = tel
                status_codes["login_success"]["password"] = password
                return HttpResponse(json.dumps(status_codes["login_success"]))
            else:
                return HttpResponse(json.dumps(status_codes["password_error"]))
        else:
            return HttpResponse(json.dumps(status_codes["user_none"]))

# 用户手机动态码登录
def login_code(request):
    if request.method == 'POST':
        user = request.body
        data = json.loads(user)
        tel = data['telephone']
        # 查询手机号是否存在
        temp = list(models.userlogin.objects.filter(telephone=tel).values())
        if(temp):
            username = models.userlogin.objects.filter(telephone=tel).values('userinfo__name').first()
            name =username["userinfo__name"]
            tel = temp[0]['telephone']
            token = make_token(tel)
            status_codes["login_success"]["token"] = token.decode()
            status_codes["login_success"]["name"] = name
            status_codes["login_success"]["telephone"] = tel
            return HttpResponse(json.dumps(status_codes["login_success"]))
        else:
            return HttpResponse(json.dumps(status_codes["user_none"]))

# 注册新用户
def add_user(request):
    # 事务处理
    from django.db import transaction
    if request.method == 'POST':
        users = json.loads(request.body)
        print(users)
        print(type(users['password']))
        users['password'] = encryption(str(users['password']))
        try:
            with transaction.atomic():
                tel_code = models.userlogin(telephone=users["telephone"],password=users["password"])
                tel_code.save()
                user = models.userlogin.objects.filter(telephone=users["telephone"])
                uid = user[0].id
                new_uinfo=models.userinfo(uid_id=uid,name=users["name"])
                new_inden=models.identification(user_id=uid,identification_type_id=1)
                new_contacts=models.emergency_contact(user_id=uid)
                new_addr=models.address(user_id=uid)
                new_inden.save()
                new_contacts.save()
                new_addr.save()
                new_uinfo.save()
                user_name = models.userinfo.objects.filter(name=users["name"])
                if (user_name):
                    token = make_token(users["telephone"])
                    status_codes["regist_ok"]["token"] = token.decode()
                    return HttpResponse(json.dumps(status_codes["regist_ok"]))
                else:
                    return HttpResponse(json.dumps(status_codes["regist_fails"]))
        except Exception as fp:
            print(fp)
            return HttpResponse(json.dumps(status_codes["regist_fails"]))

# 获取验证码
def get_code(request):
    user = request.body
    data = json.loads(user)
    print(data)
    dic = checking(data['telephone'])
    print(dic)
    return HttpResponse(json.dumps(dic))

# 忘记密码
def forget_pwd(request):
    if request.method == 'POST':
        users = json.loads(request.body)
        print(users)
        tel = users['telephone']
        users['password'] = encryption(str(users['password']))
        temp = models.userlogin.objects.filter(telephone=tel).update(password=users['password'])
        print(temp)
        if(temp):
            username = models.userlogin.objects.filter(telephone=tel).values('userinfo__name').first()
            tel_pwd = list(models.userlogin.objects.filter(telephone=tel).values())
            name = username["userinfo__name"]
            tel = tel_pwd[0]['telephone']
            pwd = tel_pwd[0]['password']
            token = make_token(tel)
            status_codes["update_success"]["token"] = token.decode()
            status_codes["update_success"]["name"] = name
            status_codes["update_success"]["telephone"] = tel
            status_codes["update_success"]["password"] = pwd
            return HttpResponse(json.dumps(status_codes["update_success"]))
        else:
            return HttpResponse(json.dumps(status_codes["update_fail"]))

# 支付接口
def alipay(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        money =data["money"]
        order = data["order"]
        """支付请求过程"""
        # 传递参数初始化支付类
        alipay = AliPay(
            appid="2016101200669809",  # 设置签约的appid
            app_notify_url="http://projectsedus.com/",  # 异步支付通知url
            app_private_key_path= ying_yong_si_yao,  # 设置应用私钥
            alipay_public_key_path=zhi_fu_bao_gong_yao,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,                                   # 设置是否是沙箱环境，True是沙箱环境
            return_url="http://localhost:8080/#/"  # 同步支付通知url
        )

        # 传递参数执行支付类里的direct_pay方法，返回签名后的支付参数，
        url = alipay.direct_pay(
            subject="乐游租车",  # 订单名称
            # 订单号生成，一般是当前时间(精确到秒)+用户ID+随机数
            out_trade_no=order,  # 订单号
            total_amount=money,  # 支付金额
            return_url="http://localhost:8080/#/"  # 支付成功后，跳转url
        )
        # 将前面后的支付参数，拼接到支付网关
    # 注意：下面支付网关是沙箱环境，
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        # print(re_url)
        # 最终进行签名后组合成支付宝的url请求
        return HttpResponse(re_url)

# 完成-个人中心用户信息显示
def get_user(request):
    if request.method == 'POST':
        data=json.loads(request.body)
        utel=data['telephone']
        users = models.userlogin.objects.filter(telephone=utel)

        print(users)
        if users:
            uid = users[0].id
            uinfo = models.userinfo.objects.filter(uid_id=uid)
            uiden = models.identification.objects.filter(user_id=uid)
            uaddr = models.address.objects.filter(user_id=uid)
            ucont = models.emergency_contact.objects.filter(user_id=uid)
            ud = {}
            ud["name"] = uinfo[0].name if uinfo else ''
            ud["identification_type_id"] = uiden[0].identification_type_id if uiden else ''
            ud["identification_num"] = uiden[0].identification_num if uiden else ''
            ud["useful_date"] = uiden[0].useful_date if uiden else ''
            ud["telephone"] = utel
            ud["email"] = uinfo[0].email if uinfo else ''
            ud["address"] = uaddr[0].address if uaddr else ''
            ud["contacts_name"] = ucont[0].contacts_name if ucont else ''
            ud["contacts_num"] = ucont[0].contacts_num if ucont else ''
            return JsonResponse(ud)
        else:
            return JsonResponse(status_codes["user_none"])
    else:
        return HttpResponse('this is Get method')
    # values返回的字典列表
    # users = models.userlogin.objects.all().values('telephone','password')
    # print(users)
    # return HttpResponse('get bufen ok')
    # values_list返回元组列表
    # users = models.userlogin.objects.all().values_list('telephone','password')
    # print(users)
    # return HttpResponse('get bufen ok')
    # 条件查询
    # users = models.userlogin.objects.filter(telephone='18874488117',password='123456')
    # for user in users:
    #     print(user.id,user.telephone,user.password)
    # return HttpResponse('you')
    # 删除
    # affect_rows=models.userlogin.objects.filter(id='3').delete()
    # 更新
    # affect_rows = models.userlogin.objects.all().update(password='123456')
    # affect_rows = models.userlogin.objects.filter(id='3').update(password='123456')
    # 大于：__gt,大于等于：__gte,小于：__lt,不等于:~Q(a=b),之一：__in,不区分大小写：__contains
    # models.userinfo.objects.filter(id__gt=1)
    # users=models.userinfo.objects.all().order_by('-id') #desc
    # Entry.objects.filter(pub_date__date__gt=datetime.date(2005, 1, 1))
