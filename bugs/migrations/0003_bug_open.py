# Generated by Django 4.1.2 on 2022-10-17 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bugs', '0002_rename_home_bug_severity'),
    ]

    operations = [
        migrations.AddField(
            model_name='bug',
            name='open',
            field=models.BooleanField(default=True),
        ),
    ]
