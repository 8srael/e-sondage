# Generated by Django 5.0.6 on 2024-05-27 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_question_type_poll_questions_question_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Possibility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'possibilities',
            },
        ),
        migrations.AlterModelTable(
            name='poll',
            table='polls',
        ),
        migrations.AlterModelTable(
            name='question',
            table='questions',
        ),
        migrations.AlterModelTable(
            name='type',
            table='types',
        ),
        migrations.AddField(
            model_name='question',
            name='possibilites',
            field=models.ManyToManyField(to='polls.possibility'),
        ),
    ]