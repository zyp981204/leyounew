from django.db import models

# Create your models here.
# 车牌
class Brand(models.Model):
    id =  models.AutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='id')
    car_brand = models.CharField(max_length=10)

# 车款
class Style(models.Model):
    style_id = models.AutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='id')
    brand_id = models.ForeignKey(db_column='brand_id',to="Brand",to_field="id",on_delete=True)
    style = models.CharField(max_length=10)
# 车辆信息
class Config(models.Model):
    style_id = models.OneToOneField(db_column='style_id',to="Style",to_field="style_id", primary_key=True,on_delete=models.CASCADE)
    seat = models.IntegerField()
    door = models.IntegerField()
    gear_box = models.CharField(max_length=255)
    output = models.CharField(max_length=255)
    drive = models.CharField(max_length=255)
    skylight = models.CharField(max_length=255)
    tank = models.CharField(max_length=255)
    radar = models.CharField(max_length=255)
    gear = models.CharField(max_length=255)
    fuel = models.CharField(max_length=255)

# 车辆主图
class MainImg(models.Model):
    id = models.AutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='id')
    style_id = models.OneToOneField(db_column='style_id',to="Style",to_field="style_id", on_delete=models.CASCADE)
    main_img = models.CharField(max_length=255)

#车辆副图
class SupImg(models.Model):
    id = models.AutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='id')
    style_id = models.ForeignKey(db_column='style_id',to="Style",to_field="style_id", on_delete=models.CASCADE)
    sup_img = models.CharField(max_length=255)
#每日保险
class DayInsu(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='id')
    style_id = models.OneToOneField(db_column='style_id', to="Style", to_field="style_id", on_delete=models.CASCADE)
    daily_insurance = models.IntegerField()
#每日租金
class DayRent(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='id')
    style_id = models.OneToOneField(db_column='style_id', to="Style", to_field="style_id", on_delete=models.CASCADE)
    daily_rental = models.IntegerField()
#押金
class Deposit(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='id')
    style_id = models.OneToOneField(db_column='style_id', to="Style", to_field="style_id", on_delete=models.CASCADE)
    deposit = models.IntegerField()

#车辆类型分类表
class TypeClassification(models.Model):
    car_type_id=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='id')
    car_type=models.CharField(max_length=255)

#车辆类型对应表
class Type(models.Model):
    id=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='id')
    type_id=models.ForeignKey(db_column='car_type_id',to="TypeClassification",to_field="car_type_id", on_delete=models.CASCADE)
    style_id = models.ForeignKey(db_column='style_id', to="Style", to_field="style_id", on_delete=models.CASCADE)