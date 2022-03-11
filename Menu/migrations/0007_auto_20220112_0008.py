# Generated by Django 3.2.11 on 2022-01-11 22:08

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Menu', '0006_table_loc'),
    ]

    operations = [
        migrations.CreateModel(
            name='order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('summary', models.FloatField(null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('payed', models.BooleanField()),
                ('table', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Menu.table')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='is_vip',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='vip_price',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.CreateModel(
            name='order_item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Menu.item')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Menu.order')),
            ],
        ),
    ]