# Generated by Django 4.2.7 on 2023-11-17 19:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0003_alter_rating_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rating",
            name="rating",
            field=models.FloatField(),
        ),
    ]
