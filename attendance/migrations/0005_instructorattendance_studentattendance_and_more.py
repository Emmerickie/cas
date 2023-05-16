# Generated by Django 4.0.3 on 2023-05-11 12:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0004_remove_attendance_attendance_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstructorAttendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_present', models.BooleanField(default=False)),
                ('lecturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='StudentAttendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_present', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='students',
        ),
        migrations.AddField(
            model_name='attendance',
            name='student',
            field=models.ManyToManyField(through='attendance.StudentAttendance', to='attendance.studentprofile'),
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='lecturer',
        ),
        migrations.AddField(
            model_name='attendance',
            name='lecturer',
            field=models.ManyToManyField(through='attendance.InstructorAttendance', to='attendance.userprofile'),
        ),
        migrations.AddField(
            model_name='studentattendance',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.attendance'),
        ),
        migrations.AddField(
            model_name='studentattendance',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.studentprofile'),
        ),
        migrations.AddField(
            model_name='instructorattendance',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.attendance'),
        ),
    ]
