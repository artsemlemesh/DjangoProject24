# Generated by Django 5.0.1 on 2024-01-12 07:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("men", "0005_category_men_cat"),
    ]

    operations = [
        migrations.AlterField(
            model_name="men",
            name="cat",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="men.category"
            ),
        ),
    ]