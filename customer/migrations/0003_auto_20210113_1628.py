# Generated by Django 3.1.1 on 2021-01-13 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_newslettersubscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newslettersubscription',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
