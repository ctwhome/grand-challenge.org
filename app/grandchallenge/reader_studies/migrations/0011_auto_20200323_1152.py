# Generated by Django 3.0.2 on 2020-03-23 11:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reader_studies", "0010_readerstudy_help_text_markdown"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="answer_type",
            field=models.CharField(
                choices=[
                    ("STXT", "Single line text"),
                    ("MTXT", "Multi line text"),
                    ("BOOL", "Bool"),
                    ("HEAD", "Heading"),
                    ("2DBB", "2D bounding box"),
                    ("DIST", "Distance measurement"),
                    ("MDIS", "Multiple distance measurements"),
                    ("POIN", "Point"),
                    ("MPOI", "Multiple points"),
                    ("POLY", "Polygon"),
                    ("MPOL", "Multiple polygons"),
                    ("CHOI", "Choice"),
                    ("MCHO", "Multiple choice"),
                ],
                default="STXT",
                max_length=4,
            ),
        ),
        migrations.CreateModel(
            name="CategoricalOption",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=1024)),
                ("default", models.BooleanField(default=False)),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="options",
                        to="reader_studies.Question",
                    ),
                ),
            ],
        ),
    ]
