# Generated by Django 4.2.14 on 2024-08-01 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("files", "0002_alter_file_author_alter_folder_author"),
    ]

    operations = [
        migrations.AlterField(
            model_name="file", name="file", field=models.FileField(upload_to=""),
        ),
    ]
