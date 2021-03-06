# Generated by Django 2.2.8 on 2019-12-13 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("algorithms", "0016_auto_20191205_1417"),
    ]

    operations = [
        migrations.AddField(
            model_name="algorithm",
            name="additional_terms",
            field=models.TextField(
                blank=True,
                help_text="By using this algortihm, users agree to the site wide terms of service. If your algorithm has any additional terms of usage, define them here.",
            ),
        ),
    ]
