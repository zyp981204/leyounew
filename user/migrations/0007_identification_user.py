# Generated by Django 2.2.5 on 2019-09-27 08:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_identification_identification_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='identification',
            name='user',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='user.userlogin'),
        ),
    ]
