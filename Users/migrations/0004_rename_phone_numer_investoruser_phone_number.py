# Generated by Django 4.2.6 on 2023-10-14 19:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0003_customeruser_phone_numer_investoruser_phone_numer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='investoruser',
            old_name='phone_numer',
            new_name='phone_number',
        ),
    ]
