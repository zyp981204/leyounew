from django.http import HttpResponse, response, JsonResponse
from django.shortcuts import render, redirect
from datetime import datetime
import json
import uuid
from django.urls import reverse
from django.core.serializers import serialize
from django.db.models import Q
from . import models
from order import models as model
from user import models as umodel


from utils.status_code import status_codes
from utils.check_tel import *
from utils.token_tool import make_token
from utils.encryption_tool import *
from utils.self_Alipay import *
from com_leyou.settings import ying_yong_si_yao, zhi_fu_bao_gong_yao

# Create your views here.

def get_typecarinfo(request):
    if request.method=='POST':
        carinfo=models.Style.objects.filter().values('style_id','style','brand_id__car_brand','mainimg__main_img','config__seat','config__drive','config__gear','dayrent__daily_rental')
        print(carinfo)
        return HttpResponse(carinfo)
    else:
        return HttpResponse('this is Get method')

def index(request):
    return HttpResponse('123')

def get_index_carinfo(request):
    if request.method=='POST':
        carinfo=models.DayRent.objects.order_by('-daily_rental')[0:6]
        car_id=json.loads(serialize('json',carinfo))
        car_id_list=[]
        for i in range(6):
            car_id_list.append(car_id[i]['fields']['style_id'])
        carinfo=models.Style.objects.filter(style_id__in=car_id_list).values('style_id','style','brand_id__car_brand','mainimg__main_img','config__seat','config__drive','config__gear','dayrent__daily_rental')
        dictcar={}
        for j in range(6):
            dictcar[str(j)]=carinfo[j]
        return JsonResponse(dictcar)
    else:
        return HttpResponse('this is Get method')

def search_carinfo(request):
    if request.method=='POST':
        data = json.loads(request.body)
        print(data)
        # {'cartypelist': [0, 0, 0, 0, 0, 0, 0, 0], 'order': 'asc', 'brand': '大众', 'price_range': [100, 300]}
        carbid=models.Brand.objects.filter(car_brand=data['brand']).values('id')
        print(carbid)
        if data['brand']=='':
            brand_carsid = models.Style.objects.all().values('style_id')
        else:
            if len(carbid)!=0:
                brand_carsid=models.Style.objects.filter(brand_id=carbid[0]['id']).values('style_id')
            else:
                return JsonResponse({"text":"此分类条件下无该品牌车辆"})
        brand_carstyleid=[]
        for i in range(len(brand_carsid)):
            brand_carstyleid.append(brand_carsid[i]['style_id'])
        # print(brand_carstyleid)
        if data['cartypelist']==[0,0,0,0,0,0,0,0]:
            data['cartypelist']=[1,1,1,1,1,1,1,1]
        for i in range(8):
            if data['cartypelist'][i]==1:
                data['cartypelist'][i]=i+1
        cartid=models.Type.objects.filter(type_id__car_type_id__in=data['cartypelist']).values('style_id').distinct()
        type_carsid=[]
        for i in range(len(cartid)):
            type_carsid.append(cartid[i]['style_id'])
        # print(type_carsid)
        carsid = [i for i in type_carsid if i in brand_carstyleid]
        # print(carsid)
        #style_id准备完毕-carsid
        if data['order']=='asc':
            sear_carinfo=models.Style.objects.filter(style_id__in=carsid,dayrent__daily_rental__range=(data['price_range'][0],data['price_range'][1])).values('style_id','style','brand_id__car_brand','mainimg__main_img','config__seat','config__drive','config__gear','dayrent__daily_rental').order_by('dayrent__daily_rental')
        else:
            sear_carinfo=models.Style.objects.filter(style_id__in=carsid,dayrent__daily_rental__range=(data['price_range'][0],data['price_range'][1])).values('style_id','style','brand_id__car_brand','mainimg__main_img','config__seat','config__drive','config__gear','dayrent__daily_rental').order_by('-dayrent__daily_rental')
        print(sear_carinfo)
        dictcar = {}
        for j in range(len(sear_carinfo)):
            dictcar[j] = sear_carinfo[j]
        return JsonResponse(dictcar)
    else:
        return HttpResponse('this is Get method')

def info_body_left(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # print(data)
        style_id = data['car_style_id']


        # sup_img的值
        s_data= serialize("json", models.SupImg.objects.filter(style_id = style_id))
        sup_img_list=[]
        for o in json.loads(s_data):
            sup_img_list.append(o["fields"]["sup_img"])
        # config配置
        c_data = serialize("json",models.Config.objects.filter(style_id = style_id))
        dic=json.loads(c_data)[0]["fields"]

        # style车款
        st_data = serialize("json",models.Style.objects.filter(style_id = style_id))
        dic1 = json.loads(st_data)[0]["fields"]

        # brand 品牌
        b_data =serialize("json",models.Brand.objects.filter(id=dic1["brand_id"]))
        dic2 = json.loads(b_data)[0]["fields"]


        dic["sup_img_list"]=sup_img_list
        dic.update(dic1)
        dic.update(dic2)
        return JsonResponse(dic)
    else:
        return HttpResponse('i love you')


def order_info(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        style_id = data['car_style_id']
        get_store_id = int(data["get_store_id"])
        return_store_id = int(data["return_store_id"])
        # dic={}
        # main_img的值
        ma_data  = serialize("json",models.MainImg.objects.filter(style_id=style_id))
        # print(ma_data)
        dic =  json.loads(ma_data)[0]["fields"]
        # style车款
        st_data = serialize("json",models.Style.objects.filter(style_id = style_id))
        dic1 = json.loads(st_data)[0]["fields"]

        # brand 品牌
        b_data =serialize("json",models.Brand.objects.filter(id=dic1["brand_id"]))
        dic2 = json.loads(b_data)[0]["fields"]

        # config配置
        c_data = serialize("json", models.Config.objects.filter(style_id=style_id))
        dic3 = json.loads(c_data)[0]["fields"]

        # get_store取车点
        g_data = serialize("json", model.store.objects.filter(id=get_store_id))
        dic4 = json.loads(g_data)[0]["fields"]

        # return_store还车点
        r_data = serialize("json", model.store.objects.filter(id=return_store_id))
        dic5 = json.loads(r_data)[0]["fields"]

        dic["get_store"]=dic4["store_name"]
        dic["return_store"]=dic5["store_name"]
        dic.update(dic1)
        dic.update(dic2)
        dic.update(dic3)


        return JsonResponse(dic)
    else:
        return HttpResponse('i love you')

def order_rent(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        style_id = data['car_style_id']
        dic={}
        # 租金rent
        r_data = serialize("json", models.DayRent.objects.filter(style_id=style_id))
        dic = json.loads(r_data)[0]["fields"]
        #押金deposit
        d_data = serialize("json", models.Deposit.objects.filter(style_id=style_id))
        dic1 = json.loads(d_data)[0]["fields"]
        #保险insu
        i_data = serialize("json", models.DayInsu.objects.filter(style_id=style_id))
        dic2 = json.loads(i_data)[0]["fields"]

        dic.update(dic1)
        dic.update(dic2)
        name = data["name"]
        # 根据用户名获得userid
        n_data = serialize("json", umodel.userinfo.objects.filter(name=name))
        n_dic = json.loads(n_data)[0]["fields"]
        dic["user_id"] = n_dic["uid"]
        return JsonResponse(dic)
    else:
        return HttpResponse('i love you')