# Generated by Django 2.2.5 on 2019-09-24 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0001_initial'),
        ('user', '0003_address_emergency_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='car.Style')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.userlogin')),
            ],
        ),
    ]
