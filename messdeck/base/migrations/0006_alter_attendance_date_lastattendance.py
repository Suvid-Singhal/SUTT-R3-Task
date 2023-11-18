# Generated by Django 4.2.7 on 2023-11-17 21:10

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0005_attendance"),
    ]

    operations = [
        migrations.AlterField(
            model_name="attendance",
            name="date",
            field=models.DateField(
                default=datetime.datetime(2023, 11, 18, 2, 39, 59, 665696)
            ),
        ),
        migrations.CreateModel(
            name="LastAttendance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "date",
                    models.DateField(
                        default=datetime.datetime(2023, 11, 18, 2, 39, 59, 665696)
                    ),
                ),
                ("meal_type", models.CharField(max_length=10)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]