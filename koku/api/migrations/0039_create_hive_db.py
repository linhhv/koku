# Generated by Django 3.1.7 on 2021-03-03 19:26
import logging
import os

from django.db import migrations


LOG = logging.getLogger(__name__)


def create_hive_db(apps, schema_editor):
    rolname = os.environ.get("HIVE_DATABASE_USER", "hive")
    datname = os.environ.get("HIVE_DATABASE_NAME", "hive")
    kokudb = os.environ.get("DATABASE_NAME", "postgres")
    kokudbuser = os.environ.get("DATABASE_USER", "postgres")
    role_check_sql = f"""
select exists (
           select 1
             from pg_roles
            where rolname = '{rolname}'
       )::boolean as "role_found";
"""
    role_create_sql = f"""
create role "{rolname}" with login encrypted password '{{hivepw}}';
"""
    role_public_revoke_sql = """
revoke connect on database "{}" from "public";
"""
    role_revoke_sql = f"""
revoke connect on database "{kokudb}" from "{rolname}";
"""
    role_grant_sql = f"""
grant connect on database "{datname}" to "{kokudbuser}";
"""
    db_check_sql = f"""
select exists (
           select 1
             from pg_database
            where datname = '{datname}'
       )::boolean as "db_found";
"""
    db_create_sql = f"""
create database "{datname}" owner "{rolname}";
"""
    db_access_check_sql = """
select has_database_privilege(%s, %s, 'connect');
"""

    with schema_editor.connection.connection.__class__(
        "postgresql://{user}:{password}@{host}:{port}/{dbname}".format(
            password=os.environ["DATABASE_PASSWORD"], **schema_editor.connection.connection.get_dsn_parameters()
        )
    ) as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(role_check_sql)
            role_exists = cur.fetchone()
            role_exists = bool(role_exists) and role_exists[0]
            cur.execute(db_check_sql)
            db_exists = cur.fetchone()
            db_exists = bool(db_exists) and db_exists[0]

            if not role_exists:
                LOG.info(f"Creating role {rolname}.")
                cur.execute(role_create_sql.format(hivepw=os.environ["HIVE_DATABASE_PASSWORD"]))
            else:
                LOG.info(f"Role {rolname} exists.")

            if not db_exists:
                LOG.info(f"Creating database {rolname}.")
                cur.execute(db_create_sql)
            else:
                LOG.info(f"Database {rolname} exists.")

            # Revoke access to koku db from public
            cur.execute(db_access_check_sql, ("public", kokudb))
            if cur.fetchone()[0]:
                LOG.info(f"Revoking public access to {kokudb}.")
                cur.execute(role_public_revoke_sql.format(kokudb))

            # Revoke access to hive db from public
            cur.execute(db_access_check_sql, ("public", datname))
            if cur.fetchone()[0]:
                LOG.info(f"Revoking public access to {datname}.")
                cur.execute(role_public_revoke_sql.format(datname))

            # Revoke access to koku db from hive user
            cur.execute(db_access_check_sql, (rolname, kokudb))
            if cur.fetchone()[0]:
                LOG.info(f"Revoking {rolname} access to {kokudb}.")
                cur.execute(role_revoke_sql)

            # Grant access to hive db from koku user
            cur.execute(db_access_check_sql, (kokudbuser, datname))
            if not cur.fetchone()[0]:
                LOG.info(f"Granting {kokudbuser} access to {datname}.")
                cur.execute(role_grant_sql)


class Migration(migrations.Migration):

    dependencies = [("api", "0038_drop_app_needs_migrations_func")]

    operations = [migrations.RunPython(create_hive_db)]
