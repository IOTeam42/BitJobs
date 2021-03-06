# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-06 10:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moneyflow', '0005_merge_20170421_2036'),
    ]

    operations = [
        migrations.CreateModel(
            name='MoneyTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(choices=[('PLN', 'PLN'), ('USD', 'USD')], max_length=3)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('date', models.DateField(auto_now_add=True)),
                ('destination_wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination', to='moneyflow.Wallet')),
                ('source_wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source', to='moneyflow.Wallet')),
            ],
        ),
    ]
