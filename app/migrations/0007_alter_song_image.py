# Generated by Django 4.2.3 on 2024-01-29 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_song_top'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/songs/%Y/%m/%d/%H/%M'),
        ),
    ]
