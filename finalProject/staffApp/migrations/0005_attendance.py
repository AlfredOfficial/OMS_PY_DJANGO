# Generated by Django 5.2.1 on 2025-05-23 12:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staffApp', '0004_role_department'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('time_in', models.TimeField(blank=True, null=True)),
                ('time_out', models.TimeField(blank=True, null=True)),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staffApp.staffprofile')),
            ],
        ),
    ]
