# Generated by Django 3.2.18 on 2023-03-16 14:04
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("reporting", "0273_ocp_on_cloud_namespace"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ocpallcostlineitemprojectdailysummaryp",
            name="namespace",
            field=models.CharField(max_length=253, null=True),
        ),
    ]