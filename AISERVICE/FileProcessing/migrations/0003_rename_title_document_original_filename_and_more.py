# Generated by Django 5.2.4 on 2025-07-25 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FileProcessing', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='document',
            old_name='title',
            new_name='original_filename',
        ),
        migrations.RemoveField(
            model_name='document',
            name='processed',
        ),
        migrations.AddField(
            model_name='document',
            name='error_message',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='document',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('processing', 'Processing'), ('ready', 'Ready'), ('error', 'Error')], default='pending', max_length=20),
        ),
    ]
