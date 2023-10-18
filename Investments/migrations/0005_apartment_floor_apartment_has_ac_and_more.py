# Generated by Django 4.2.6 on 2023-10-18 16:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Investments', '0004_investment_resized_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='floor',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(20)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='apartment',
            name='has_AC',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='apartment',
            name='has_balcony',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='apartment',
            name='has_basement',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='apartment',
            name='has_garage',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='apartment',
            name='has_garden',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='apartment',
            name='price',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1, message='Value must be greater than 0'), django.core.validators.MaxValueValidator(100000000, message='Value cannot exceed 100 million')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='apartment',
            name='two_floor_apartment',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
    ]
