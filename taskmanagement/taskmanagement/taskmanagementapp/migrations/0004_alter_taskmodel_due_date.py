# Generated by Django 4.1 on 2023-09-12 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanagementapp', '0003_alter_taskmodel_assigned_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskmodel',
            name='due_date',
            field=models.DateField(),
        ),
    ]
