# Generated by Django 4.1.5 on 2023-01-24 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="cover",
            field=models.ImageField(upload_to="files/"),
        ),
    ]
