# Generated by Django 3.2 on 2023-05-07 08:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_review'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='question',
        ),
        migrations.DeleteModel(
            name='SurveyResult',
        ),
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]