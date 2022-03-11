# Generated by Django 3.2.11 on 2022-01-22 20:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Menu', '0012_alter_payment_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='credit_num',
            field=models.CharField(default=4111111111111111, max_length=300, validators=[django.core.validators.RegexValidator('^(?:4[0-9]{12}(?:[0-9]{3})?|[25][1-7][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\\d{3})\\d{11})$')]),
            preserve_default=False,
        ),
    ]
