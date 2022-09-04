# Generated by Django 4.1 on 2022-09-04 20:57

import company.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("company", "0002_alter_company_ulke"),
    ]

    operations = [
        migrations.AlterField(
            model_name="company",
            name="kurulus_logo",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=company.models.upload_logo,
                verbose_name="Kuruluş Logo",
            ),
        ),
    ]