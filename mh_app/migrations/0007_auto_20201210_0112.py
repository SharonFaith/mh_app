# Generated by Django 3.1.3 on 2020-12-09 22:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mh_app', '0006_auto_20201210_0108'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mhproprofile',
            old_name='work_contact',
            new_name='work_place_contact',
        ),
    ]
