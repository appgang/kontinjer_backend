# Generated by Django 3.1.6 on 2021-02-21 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0004_auto_20210220_2330'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trashcan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material', models.CharField(default='', max_length=100)),
                ('latitude', models.CharField(default='', max_length=100)),
                ('longitude', models.CharField(default='', max_length=100)),
            ],
        ),
    ]
