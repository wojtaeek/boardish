# Generated by Django 5.1.4 on 2025-01-21 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0004_alter_board_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='element',
            name='type',
            field=models.CharField(choices=[('button', 'Button'), ('text', 'Text'), ('image', 'Image'), ('clock', 'Clock'), ('paint', 'Paint'), ('custom', 'Custom')], default='custom', max_length=50),
        ),
    ]
