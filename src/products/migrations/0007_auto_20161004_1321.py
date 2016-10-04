# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20161004_1320'),
    ]

    operations = [
        migrations.RenameField(
            model_name='variation',
            old_name='invetory',
            new_name='inventory',
        ),
    ]
