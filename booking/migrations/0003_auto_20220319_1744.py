# Generated by Django 3.2.7 on 2022-03-19 17:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_auto_20220319_1120'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='calendarevent',
            options={},
        ),
        migrations.DeleteModel(
            name='EventReceiver',
        ),
    ]
