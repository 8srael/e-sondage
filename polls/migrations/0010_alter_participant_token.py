# Generated by Django 5.0.6 on 2024-06-13 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_participant_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='token',
            field=models.UUIDField(blank=True, editable=False, unique=True),
        ),
    ]