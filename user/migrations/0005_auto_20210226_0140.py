# Generated by Django 3.1.6 on 2021-02-26 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20210226_0115'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='years_saved',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='profile',
            name='recycled',
            field=models.IntegerField(default=0),
        ),
    ]
