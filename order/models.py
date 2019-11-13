from django.db import models
import car.models as car
import user.models as user
# Create your models here.
class store(models.Model):
    store_name=models.CharField(max_length=255)
    store_address=models.CharField(max_length=255)
    store_tel=models.CharField(max_length=255)
    store_info=models.CharField(max_length=255)

class store_inventory(models.Model):
    car_style=models.ForeignKey(to='car.Style',to_field='style_id',on_delete=models.CASCADE)
    store=models.ForeignKey(to='store',to_field='id',on_delete=models.CASCADE)
    inventory=models.IntegerField()

class auditor(models.Model):
    name=models.CharField(max_length=255)

class userorder(models.Model):
    order_id=models.AutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='id')
    user=models.ForeignKey(to='user.userlogin',to_field='id',on_delete=models.CASCADE)
    getstore=models.ForeignKey(to='store',to_field='id',on_delete=models.CASCADE,related_name='getstore')
    returnstore=models.ForeignKey(to='store',to_field='id',on_delete=models.CASCADE,related_name='returnstore')
    rental_start_date=models.DateField()
    rental_end_date=models.DateField()
    rental_costs=models.IntegerField()
    payment_status=models.IntegerField()
    auditor=models.ForeignKey(to='auditor',to_field='id',on_delete=models.CASCADE)
    car_style=models.ForeignKey(to='car.Style',to_field='style_id',on_delete=models.CASCADE)

class tenant_info(models.Model):
    order=models.ForeignKey(to='userorder',to_field='order_id',on_delete=models.CASCADE)
    tenant_name=models.CharField(max_length=255)
    identification_type=models.ForeignKey(to='user.identification_type',to_field='id',on_delete=models.CASCADE)
    identification_num=models.CharField(max_length=255)