# Generated by Django 4.0.3 on 2023-05-22 18:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0007_alter_schedule_end_time_alter_schedule_start_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgrammeCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_type', models.CharField(choices=[('E', 'Elective'), ('C', 'Core')], max_length=1)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.course')),
                ('programme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.programme')),
            ],
        ),
    ]
