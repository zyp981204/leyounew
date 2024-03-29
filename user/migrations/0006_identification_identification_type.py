# Generated by Django 2.2.5 on 2019-09-24 11:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20190924_1935'),
    ]

    operations = [
        migrations.CreateModel(
            name='identification_type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='identification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identification_num', models.CharField(max_length=255)),
                ('useful_date', models.DateField()),
                ('identification_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.identification_type')),
            ],
        ),
    ]
