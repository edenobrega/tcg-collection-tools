# Generated by Django 4.1.1 on 2022-09-26 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0009_card_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='image_flipped',
            field=models.URLField(null=True),
        ),
    ]
