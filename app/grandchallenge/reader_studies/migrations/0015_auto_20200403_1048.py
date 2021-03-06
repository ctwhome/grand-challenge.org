# Generated by Django 3.0.2 on 2020-04-03 10:48
import uuid

import django.contrib.postgres.fields.jsonb
import django.db.models.deletion
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("reader_studies", "0014_readerstudy_case_text"),
    ]

    operations = [
        migrations.AddField(
            model_name="readerstudy",
            name="allow_answer_modification",
            field=models.BooleanField(
                default=False,
                help_text="If true, readers are allowed to modify their answers for a case by navigating back to previous cases. 'allow_case_browsing' must be checked with this as well.",
            ),
        ),
        migrations.AddField(
            model_name="readerstudy",
            name="allow_case_navigation",
            field=models.BooleanField(
                default=False,
                help_text="If true, readers are allowed to navigate back and forth between cases in this reader study.",
            ),
        ),
        migrations.CreateModel(
            name="HistoricalAnswer",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_index=True, default=uuid.uuid4, editable=False
                    ),
                ),
                ("answer", django.contrib.postgres.fields.jsonb.JSONField()),
                (
                    "history_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("history_date", models.DateTimeField()),
                (
                    "history_change_reason",
                    models.CharField(max_length=100, null=True),
                ),
                (
                    "history_type",
                    models.CharField(
                        choices=[
                            ("+", "Created"),
                            ("~", "Changed"),
                            ("-", "Deleted"),
                        ],
                        max_length=1,
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "historical answer",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": "history_date",
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
