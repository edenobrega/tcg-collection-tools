# Generated by Django 4.1.1 on 2022-09-26 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0008_card_converted_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='image',
            field=models.URLField(null=True),
        ),
    ]
