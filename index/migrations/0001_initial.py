# Generated by Django 4.1.3 on 2022-11-24 08:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('number', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(verbose_name='Date Created')),
                ('title_text', models.CharField(max_length=40)),
                ('owner_text', models.CharField(max_length=40)),
                ('description_text', models.CharField(max_length=200)),
                ('date', models.DateField(verbose_name='Date')),
                ('start_date', models.TimeField(verbose_name='Start')),
                ('end_date', models.TimeField(verbose_name='End')),
            ],
        ),
        migrations.CreateModel(
            name='userMeeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.meeting')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_subject', models.CharField(max_length=5)),
                ('class_number', models.CharField(max_length=5)),
                ('class_section', models.CharField(max_length=5)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserBio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(default='This is the default bio', max_length=500)),
                ('degree', models.CharField(default='Unknown', max_length=200)),
                ('year', models.CharField(default='Unknown', max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_text', models.CharField(max_length=200)),
                ('context_username', models.CharField(default='error', max_length=200)),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.meeting')),
            ],
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addee_uid', models.CharField(max_length=150)),
                ('addee_nom', models.CharField(max_length=150)),
                ('adder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
