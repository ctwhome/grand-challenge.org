# Generated by Django 3.0.2 on 2020-02-27 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("submission_conversion", "0002_auto_20181031_1043"),
    ]

    operations = [
        migrations.AddField(
            model_name="submissiontoannotationsetjob",
            name="completed_at",
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name="submissiontoannotationsetjob",
            name="started_at",
            field=models.DateTimeField(null=True),
        ),
    ]