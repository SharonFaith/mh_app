# Generated by Django 3.1.3 on 2020-12-10 07:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mh_app', '0014_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='person_reviewing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='mh_app.mhproprofile'),
        ),
    ]
