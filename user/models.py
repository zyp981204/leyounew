from django.db import models
import car.models as car
# Create your models here.
class userlogin(models.Model):
    telephone=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    def add(self):
        self.save()

class userinfo(models.Model):
    name=models.CharField(max_length=255)
    email=models.EmailField()
    uid=models.ForeignKey(to="userlogin",to_field="id",on_delete=models.CASCADE)

class emergency_contact(models.Model):
    user=models.ForeignKey(to="userlogin",to_field="id",on_delete=models.CASCADE)
    contacts_name=models.CharField(max_length=255)
    contacts_num=models.CharField(max_length=255)

class address(models.Model):
    user=models.ForeignKey(to="userlogin",to_field="id",on_delete=models.CASCADE)
    address=models.CharField(max_length=255)

class collection(models.Model):
    user=models.ForeignKey(to="userlogin",to_field="id",on_delete=models.CASCADE)
    car_style=models.ForeignKey(to="car.Style",to_field="style_id",on_delete=models.CASCADE)

class identification_type(models.Model):
    type=models.CharField(max_length=255)

class identification(models.Model):
    identification_type=models.ForeignKey(to="identification_type",to_field="id",on_delete=models.CASCADE)
    identification_num=models.CharField(max_length=255)
    useful_date=models.DateField()
    user=models.ForeignKey(to="userlogin",to_field="id",on_delete=models.CASCADE)