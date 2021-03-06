# Generated by Django 3.0.10 on 2020-10-02 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("algorithms", "0027_delete_result"),
    ]

    operations = [
        migrations.AddField(
            model_name="algorithm",
            name="result_template",
            field=models.TextField(
                blank=True,
                default="<pre>{{ result_dict|tojson(indent=2) }}</pre>",
                help_text="Define the jinja template to render the content of the result.json to html. For example, the following template will print out all the keys and values of the result.json. Use result-dict to accessthe json root.{% for key, value in result_dict.metrics.items() -%}{{ key }}  {{ value }}{% endfor %}",
            ),
        ),
    ]
