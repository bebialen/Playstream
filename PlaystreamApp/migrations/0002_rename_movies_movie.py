# Generated by Django 4.2.5 on 2023-09-29 11:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PlaystreamApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Movies',
            new_name='Movie',
        ),
    ]