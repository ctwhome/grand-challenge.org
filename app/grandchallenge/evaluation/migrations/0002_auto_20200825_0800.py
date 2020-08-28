# Generated by Django 3.0.9 on 2020-08-25 08:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("algorithms", "0027_delete_result"),
        ("components", "0001_initial"),
        ("challenges", "0024_auto_20200611_1053"),
        ("evaluation", "0001_squashed_0033_auto_20200816_1357"),
    ]

    operations = [
        migrations.RenameModel(old_name="Config", new_name="Phase",),
        migrations.AlterField(
            model_name="phase",
            name="challenge",
            field=models.ForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                to="challenges.Challenge",
            ),
        ),
        migrations.AddField(
            model_name="method",
            name="phase",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="evaluation.Phase",
            ),
        ),
        migrations.AddField(
            model_name="submission",
            name="phase",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="evaluation.Phase",
            ),
        ),
        migrations.AlterField(
            model_name="method",
            name="challenge",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="challenges.Challenge",
            ),
        ),
        migrations.AlterField(
            model_name="submission",
            name="challenge",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="challenges.Challenge",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="submission",
            unique_together={("phase", "predictions_file", "algorithm_image")},
        ),
    ]
