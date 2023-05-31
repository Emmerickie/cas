# Generated by Django 4.0.3 on 2023-05-27 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0013_remove_attendance_course_attendance_lesson'),
    ]

    operations = [
        migrations.AddField(
            model_name='programmecourse',
            name='level',
            field=models.CharField(choices=[('1', 'First Year'), ('2', 'Second Year'), ('3', 'Third Year'), ('4', 'Fourth Year')], default=3, max_length=1),
            preserve_default=False,
        ),
    ]
