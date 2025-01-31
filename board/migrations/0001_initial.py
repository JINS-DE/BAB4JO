# Generated by Django 4.1.4 on 2023-01-10 07:36

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BoardTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.CharField(max_length=300)),
                ('save_date', models.DateField(default=django.utils.timezone.now)),
                ('file_name', models.CharField(blank=True, max_length=100)),
                ('user_name', models.CharField(max_length=100)),
                ('hit', models.IntegerField(default=0)),
                ('likes', models.ManyToManyField(related_name='likes', to=settings.AUTH_USER_MODEL)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='board', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ReplyTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('content', models.CharField(max_length=300)),
                ('save_date', models.DateField(default=datetime.datetime.now)),
                ('write_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='board.boardtable')),
                ('write_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
