# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_variations'),
    ]

    operations = [
        migrations.CreateModel(
            name='Variation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('sale_price', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('active', models.BooleanField(default=True)),
                ('invnetory', models.IntegerField(blank=True, null=True)),
                ('product', models.ForeignKey(to='products.Product')),
            ],
        ),
        migrations.RemoveField(
            model_name='variations',
            name='product',
        ),
        migrations.DeleteModel(
            name='Variations',
        ),
    ]
