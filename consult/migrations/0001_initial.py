# Generated by Django 4.2.7 on 2023-11-19 17:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appnt_type', models.CharField(choices=[('CALLBACK', 'CALLBACK'), ('MEASUREMENT', 'MEASUREMENT'), ('CONSULTATION', 'CONSULTATION'), ('DRAFT', 'DRAFT')], default='CALLBACK', max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('time', models.TimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
