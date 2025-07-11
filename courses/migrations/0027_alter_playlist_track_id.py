# Generated by Django 5.1.5 on 2025-02-01 14:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0026_playlist_track_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='track_id',
            field=models.ForeignKey(blank=True, db_column='track_id', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='playlists', to='courses.tracks'),
        ),
    ]
