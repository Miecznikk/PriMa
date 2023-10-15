# Generated by Django 4.2.6 on 2023-10-15 16:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Investments', '0002_rename_apartment_numer_apartment_apartment_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='investment',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Investments.investment'),
            preserve_default=False,
        ),
    ]