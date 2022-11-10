# Generated by Django 4.0.8 on 2022-10-17 22:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('collection', '0016_alter_card_collector_number_alter_card_power_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Card',
            new_name='MTG_Card',
        ),
        migrations.RenameModel(
            old_name='CardType',
            new_name='MTG_CardType',
        ),
        migrations.RenameModel(
            old_name='MTGCollected',
            new_name='MTG_Collected',
        ),
        migrations.RenameModel(
            old_name='Set',
            new_name='MTG_Set',
        ),
        migrations.RenameModel(
            old_name='SetType',
            new_name='MTG_SetType',
        ),
        migrations.RenameModel(
            old_name='TypeLine',
            new_name='MTG_TypeLine',
        ),
        migrations.AlterField(
            model_name='mtg_card',
            name='rarity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collection.mtg_rarity'),
        ),
    ]