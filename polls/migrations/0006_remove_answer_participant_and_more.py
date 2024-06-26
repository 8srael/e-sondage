# Generated by Django 5.0.6 on 2024-06-26 22:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_alter_questionpossibility_possibility'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='participant',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='has_submitted',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='poll',
        ),
        migrations.CreateModel(
            name='PollParticipant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('has_submitted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.participant')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.poll')),
            ],
            options={
                'verbose_name_plural': 'Polls-Participants',
                'db_table': 'polls_participants',
            },
        ),
        migrations.AddField(
            model_name='answer',
            name='poll_participant',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='polls.pollparticipant'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='participant',
            name='polls',
            field=models.ManyToManyField(blank=True, through='polls.PollParticipant', to='polls.poll'),
        ),
        migrations.AddField(
            model_name='poll',
            name='participants',
            field=models.ManyToManyField(blank=True, through='polls.PollParticipant', to='polls.participant'),
        ),
    ]
