# Generated by Django 2.1.2 on 2019-03-18 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20190318_1017'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChangeLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tem', models.CharField(max_length=5)),
                ('pre', models.CharField(max_length=6)),
                ('hum', models.CharField(max_length=5)),
                ('led', models.CharField(max_length=5)),
                ('lasttime', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ViewParam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tem', models.CharField(max_length=5)),
                ('pre', models.CharField(max_length=6)),
                ('hum', models.CharField(max_length=5)),
                ('led', models.CharField(max_length=5)),
                ('lasttime', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
