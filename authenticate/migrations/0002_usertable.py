# Generated by Django 3.2.4 on 2021-07-16 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FirstName', models.CharField(max_length=255, null=True)),
                ('LastName', models.CharField(max_length=255, null=True)),
                ('Email', models.CharField(max_length=255, null=True)),
                ('Password', models.CharField(max_length=255, null=True)),
            ],
        ),
    ]
