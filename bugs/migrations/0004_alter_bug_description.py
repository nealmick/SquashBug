# Generated by Django 4.1.2 on 2022-10-17 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bugs', '0003_bug_open'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bug',
            name='description',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]