# Generated by Django 3.1.3 on 2020-12-09 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mh_app', '0004_user_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='mhproprofile',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
