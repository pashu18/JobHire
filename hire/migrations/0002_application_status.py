# Generated by Django 5.2.3 on 2025-06-25 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hire', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('reviewed', 'Reviewed'), ('rejected', 'Rejected')], default='pending', max_length=10),
        ),
    ]
