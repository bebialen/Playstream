# Generated by Django 4.2.5 on 2023-10-11 05:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('PlaystreamApp', '0013_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecentMovie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('watched_movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PlaystreamApp.movie')),
            ],
        ),
        migrations.CreateModel(
            name='RecentEpisode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('watched_episode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PlaystreamApp.episode')),
            ],
        ),
    ]