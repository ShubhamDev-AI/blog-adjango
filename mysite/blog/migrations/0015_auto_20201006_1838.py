# Generated by Django 3.1.1 on 2020-10-06 13:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0014_auto_20201006_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='user_like',
            field=models.ManyToManyField(blank=True, related_name='post_liked', to=settings.AUTH_USER_MODEL),
        ),
    ]
