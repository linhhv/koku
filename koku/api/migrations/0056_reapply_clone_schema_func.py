# Generated by Django 3.2.12 on 2022-04-05 18:05
import os

from django.db import migrations

from koku import migration_sql_helpers as msh


def apply_public_clone_func_update(apps, schema_editor):
    path = msh.find_db_functions_dir()
    msh.apply_sql_file(schema_editor, os.path.join(path, "clone_schema.sql"), literal_placeholder=True)


class Migration(migrations.Migration):

    dependencies = [("api", "0055_install_pg_stat_statements")]

    operations = [migrations.RunPython(code=apply_public_clone_func_update, reverse_code=migrations.RunPython.noop)]
