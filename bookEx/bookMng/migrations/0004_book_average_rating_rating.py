# Generated by Django 5.0.4 on 2024-05-06 06:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bookMng", "0003_comment"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="average_rating",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=3, null=True
            ),
        ),
        migrations.CreateModel(
            name="Rating",
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
                ("stars", models.IntegerField()),
                ("review", models.TextField()),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="bookMng.book"
                    ),
                ),
            ],
        ),
    ]
