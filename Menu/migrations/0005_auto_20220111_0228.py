# Generated by Django 3.2.11 on 2022-01-11 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Menu', '0004_alter_item_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='table',
            name='reserve',
            field=models.BooleanField(default=False),
        ),
    ]
