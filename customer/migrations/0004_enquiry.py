# Generated by Django 3.1.1 on 2021-01-15 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_auto_20210113_1628'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enquiry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=150, null=True)),
                ('last_name', models.CharField(blank=True, max_length=150, null=True)),
                ('email', models.EmailField(help_text='Your email address', max_length=254)),
                ('contact_number', models.IntegerField(blank=True, null=True)),
                ('message', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
