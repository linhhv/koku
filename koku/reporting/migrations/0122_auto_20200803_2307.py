# Generated by Django 2.2.14 on 2020-08-03 23:07
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [("reporting", "0121_auto_20200728_2258")]

    operations = [
        migrations.AlterField(
            model_name="azurecostentryproductservice", name="consumed_service", field=models.TextField(null=True)
        ),
        migrations.AlterField(
            model_name="azurecostentryproductservice", name="resource_group", field=models.TextField(null=True)
        ),
        migrations.AlterField(
            model_name="azurecostentryproductservice", name="resource_type", field=models.TextField(null=True)
        ),
    ]