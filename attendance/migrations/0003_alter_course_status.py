# Generated by Django 4.0.3 on 2023-03-26 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0002_alter_department_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (2, 'Inactive')], default=1),
        ),
    ]
