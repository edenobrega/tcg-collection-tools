# Generated by Django 4.0.8 on 2022-10-04 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0014_alter_card_mana_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='flavor',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='text',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
