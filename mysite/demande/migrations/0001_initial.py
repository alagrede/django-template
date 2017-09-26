# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(null=True, verbose_name='Date')),
                ('obj', models.CharField(max_length=200, null=True, verbose_name='Object')),
                ('state', models.SmallIntegerField(null=True, verbose_name='State', choices=[(1, 'Todo'), (2, 'Done')])),
                ('printed_doc', models.BooleanField(default=False, verbose_name=b'printed document')),
                ('author', models.ForeignKey(related_name='auteur', verbose_name='Author', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Task',
                'verbose_name_plural': 'Tasks',
            },
        ),
    ]
