# Generated by Django 4.2.5 on 2023-09-30 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanagementapp', '0004_alter_taskmodel_due_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskmodel',
            name='comments',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
