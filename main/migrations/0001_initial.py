# Generated by Django 4.0.4 on 2022-10-25 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_url', models.TextField()),
                ('service_login', models.CharField(max_length=30)),
                ('service_password', models.CharField(max_length=30)),
            ],
        ),
    ]
