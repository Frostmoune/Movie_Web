# Generated by Django 2.0.3 on 2018-05-23 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Movies', '0002_remove_movie_search_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='search_tag',
            field=models.TextField(default='Null'),
        ),
    ]
