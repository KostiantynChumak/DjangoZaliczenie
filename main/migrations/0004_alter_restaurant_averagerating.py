# Generated by Django 3.2.4 on 2021-06-13 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_restaurant_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='averageRating',
            field=models.FloatField(default=0),
        ),
    ]
