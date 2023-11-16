# Generated by Django 4.2.7 on 2023-11-16 16:44

import airport.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("airport", "0003_alter_route_unique_together"),
    ]

    operations = [
        migrations.AddField(
            model_name="airplane",
            name="image",
            field=models.ImageField(
                null=True, upload_to=airport.models.airplane_image_file_path
            ),
        ),
    ]