# Generated by Django 2.2.5 on 2019-09-24 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_identification_identification_type'),
        ('car', '0001_initial'),
        ('order', '0002_auditor'),
    ]

    operations = [
        migrations.CreateModel(
            name='userorder',
            fields=[
                ('order_id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='id')),
                ('rental_start_date', models.DateField()),
                ('rental_end_date', models.DateField()),
                ('rental_costs', models.IntegerField()),
                ('payment_status', models.IntegerField()),
                ('auditor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.auditor')),
                ('car_style', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='car.Style')),
                ('getstore', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='getstore', to='order.store')),
                ('returnstore', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='returnstore', to='order.store')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.userlogin')),
            ],
        ),
    ]
