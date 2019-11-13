from django.http import HttpResponse, response, JsonResponse
from django.shortcuts import render, redirect
from datetime import datetime
import json
import uuid
from django.urls import reverse
from django.core.serializers import serialize
from django.db.models import Q
from car import models as model
from user import models as umodel
from . import models
from utils.self_Alipay import *
from com_leyou.settings import ying_yong_si_yao, zhi_fu_bao_gong_yao

# Create your views here.

def user_order(request):
    return HttpResponse('user_order')


def select(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        order_id = data['order_id']
        # order中的数据
        o_data = serialize("json", models.userorder.objects.filter(order_id=order_id))
        dic = json.loads(o_data)[0]["fields"]
        #租车人tenant
        t_data = serialize("json", models.tenant_info.objects.filter(order_id=order_id))
        dic1 = json.loads(t_data)[0]["fields"]

        # 租车地址
        s_data =serialize("json", models.store.objects.filter(id=dic["getstore"]))
        dic2 = json.loads(s_data)[0]["fields"]
        #还车地址
        r_data = serialize("json", models.store.objects.filter(id=dic["returnstore"]))
        dic3 = json.loads(r_data)[0]["fields"]
        # 车款style
        b_data = serialize("json", model.Style.objects.filter(style_id=dic["car_style"]))
        dic4 = json.loads(b_data)[0]["fields"]
        #车辆配置config
        c_data = serialize("json", model.Config.objects.filter(style_id=dic["car_style"]))
        dic5 = json.loads(c_data)[0]["fields"]
        # 品牌brand
        br_data = serialize("json", model.Brand.objects.filter(id=dic4["brand_id"]))
        dic6 = json.loads(br_data)[0]["fields"]

        dic["get_store"]=dic2["store_name"]
        dic["return_store"]=dic3["store_name"]
        dic.update(dic1)
        dic.update(dic4)
        dic.update(dic5)
        dic.update(dic6)
        return JsonResponse(dic)
    else:
        return HttpResponse('i love you')

# 插入order以及tenant
def insert(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # 产生随机数order_id
        ran = random_order()
        data["insert_order"]["order_id"]=ran
        data["insert_tenant"]["order_id"]=ran
        # print(data)
        # print(type(data))
        models.userorder.objects.update_or_create(**data["insert_order"])

        models.tenant_info.objects.update_or_create(**data["insert_tenant"])
        dict1 = {}
        dict1["order_id"] = ran
        #
        # i_data = serialize("json", models.store_inventory.objects.filter(car_style_id=data["insert_order"]["car_style_id"],store_id=data["insert_order"]["getstore_id"]))
        # inventory = json.loads(i_data)[0]["fields"]["inventory"]
        # models.store_inventory.objects.filter(car_style_id=data["insert_order"]["car_style_id"],store_id=data["insert_order"]["getstore_id"]).update(inventory=inventory-1)
        return JsonResponse(dict1)

# 生成随机数order_id
def random_order():
    import random
    import time
    # 随机七位数
    # rd_seven = random.random()*10
    # rd_seven = str(int(rd_seven))
    # 获取当前时间戳
    time_now = time.time()
    time_now = str(int(time_now))
    # result = rd_seven+time_now
    result = time_now

    return int(result)


# 查找用户userid

def user_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data["name"]
        # 根据用户名获得userid
        n_data = serialize("json",umodel.userinfo.objects.filter(name=name))
        n_dic = json.loads(n_data)[0]["fields"]
        user_id = n_dic["uid"]
        # 获取订单数量
        o_count = models.userorder.objects.filter(user_id=user_id).count()
        ud={}
        list = []

        if o_count>0:
            if "index" in data:

                index = data["index"]
            #     订单
                o_data = serialize("json", models.userorder.objects.filter(user_id=user_id))
                dic = json.loads(o_data)[index]["fields"]
                id_list = models.userorder.objects.filter(user_id=user_id).values("order_id")
                dic.update(id_list[index])
                #车款
                s_data = serialize("json", model.Style.objects.filter(style_id=dic["car_style"]))
                dic1 = json.loads(s_data)[0]["fields"]
                #车配置
                c_data = serialize("json", model.Config.objects.filter(style_id=dic["car_style"]))
                dic2 = json.loads(c_data)[0]["fields"]

                #车图
                m_data = serialize("json", model.MainImg.objects.filter(style_id=dic["car_style"]))
                # print(m_data)
                dic3 = json.loads(m_data)[0]["fields"]
                dic.update(dic1)
                dic.update(dic2)
                dic.update(dic3)
                ud.update(dic)
                for i in range(o_count):
                    list.append(i)
            ud["list"]=list
            ud["order"] = 1
            print(ud)
            return JsonResponse(ud)

        else:

            ud["order"]=0
            return JsonResponse(ud)

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
            return_url="http://localhost:8080/#/successorder?ispay=1"  # 同步支付通知url
        )

        # 传递参数执行支付类里的direct_pay方法，返回签名后的支付参数，
        url = alipay.direct_pay(
            subject="乐游租车",  # 订单名称
            # 订单号生成，一般是当前时间(精确到秒)+用户ID+随机数
            out_trade_no=order,  # 订单号
            total_amount=money,  # 支付金额
            return_url="http://localhost:8080/#/successorder?ispay=1"  # 支付成功后，跳转url
        )
        # 将前面后的支付参数，拼接到支付网关
    # 注意：下面支付网关是沙箱环境，
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        # print(re_url)
        # 最终进行签名后组合成支付宝的url请求
        return HttpResponse(re_url)