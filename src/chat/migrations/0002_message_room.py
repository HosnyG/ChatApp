# Generated by Django 4.0 on 2021-12-11 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='room',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
