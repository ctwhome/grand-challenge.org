# Generated by Django 3.1.1 on 2020-10-20 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reader_studies", "0023_auto_20201020_1027"),
    ]

    operations = [
        migrations.AddField(
            model_name="readerstudy",
            name="validate_hanging_list",
            field=models.BooleanField(default=True),
        ),
    ]
