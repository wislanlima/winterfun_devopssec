# Generated by Django 3.2.7 on 2022-03-21 21:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0005_alter_event_accounts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='accounts',
            field=models.ManyToManyField(blank=True, help_text='The accounts this event belongs to. A event will be sent to all accounts granted to each of their accounts.', related_name='event_set', related_query_name='account', to=settings.AUTH_USER_MODEL, verbose_name='accounts'),
        ),
    ]
