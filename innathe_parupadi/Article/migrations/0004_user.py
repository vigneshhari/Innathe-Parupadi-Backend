# Generated by Django 2.0.2 on 2018-02-04 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Article', '0003_auto_20180203_1749'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('passhash', models.CharField(max_length=1000)),
            ],
        ),
    ]
