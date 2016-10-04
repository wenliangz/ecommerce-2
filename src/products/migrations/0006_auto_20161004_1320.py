# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20161004_1208'),
    ]

    operations = [
        migrations.RenameField(
            model_name='variation',
            old_name='invnetory',
            new_name='invetory',
        ),
    ]
