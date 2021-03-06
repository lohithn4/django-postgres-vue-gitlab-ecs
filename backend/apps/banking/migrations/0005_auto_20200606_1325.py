# Generated by Django 3.0.6 on 2020-06-06 13:25

import backend.storage_backends
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("banking", "0004_transaction_source_file"),
    ]

    operations = [
        migrations.AlterField(
            model_name="statementfile",
            name="statement_file",
            field=models.FileField(
                storage=backend.storage_backends.PrivateMediaStorage,
                upload_to="banking",
            ),
        ),
    ]
