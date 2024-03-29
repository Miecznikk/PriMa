# Generated by Django 4.2.6 on 2023-10-14 19:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_investoruser'),
    ]

    operations = [
        migrations.AddField(
            model_name='customeruser',
            name='phone_numer',
            field=models.CharField(max_length=9, null=True, validators=[django.core.validators.RegexValidator(code='Invalid phone number', regex='^\\d{9}$')]),
        ),
        migrations.AddField(
            model_name='investoruser',
            name='phone_numer',
            field=models.CharField(default='790909090', max_length=9, validators=[django.core.validators.RegexValidator(code='Invalid phone number', regex='^\\d{9}$')]),
            preserve_default=False,
        ),
    ]
