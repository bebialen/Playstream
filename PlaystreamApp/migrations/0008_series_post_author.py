# Generated by Django 4.2.5 on 2023-10-07 09:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('PlaystreamApp', '0007_movie_post_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='series',
            name='post_author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]