# Generated by Django 3.0.1 on 2020-01-23 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0002_remove_post_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='published',
            field=models.BooleanField(default=False),
        ),
    ]
