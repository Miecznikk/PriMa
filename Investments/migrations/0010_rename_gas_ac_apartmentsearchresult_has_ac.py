# Generated by Django 4.2.6 on 2023-10-24 16:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Investments', '0009_apartmentsearchresult_max_rooms'),
    ]

    operations = [
        migrations.RenameField(
            model_name='apartmentsearchresult',
            old_name='gas_AC',
            new_name='has_AC',
        ),
    ]
