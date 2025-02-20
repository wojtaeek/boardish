# Generated by Django 5.1.4 on 2025-01-09 21:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0002_board_element_userboard_board_user_boardelement'),
    ]

    operations = [
        migrations.AddField(
            model_name='element',
            name='board',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='elements', to='boards.board'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='element',
            name='order',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='BoardElement',
        ),
    ]
