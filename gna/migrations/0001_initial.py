# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DailyCache',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=255, db_index=True)),
                ('date', models.DateField()),
                ('value', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'gna_daily_cache',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DailyFlagCache',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=255, db_index=True)),
                ('date', models.DateField()),
                ('value', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'gna_daily_flag_cache',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DeltaCache',
            fields=[
                ('key', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('datetime', models.DateTimeField()),
                ('value', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'gna_delta_cache',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SimpleCache',
            fields=[
                ('key', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('value', models.CharField(max_length=255, null=True)),
            ],
            options={
                'db_table': 'gna_simple_cache',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='dailyflagcache',
            unique_together=set([('key', 'date')]),
        ),
        migrations.AlterUniqueTogether(
            name='dailycache',
            unique_together=set([('key', 'date')]),
        ),
    ]
