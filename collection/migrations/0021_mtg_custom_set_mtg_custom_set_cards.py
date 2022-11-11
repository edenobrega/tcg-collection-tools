# Generated by Django 4.0.8 on 2022-11-10 17:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('collection', '0020_alter_mtg_card_artist_alter_mtg_card_mana_cost_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MTG_Custom_Set',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=2000)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MTG_Custom_Set_Cards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collection.mtg_card')),
                ('custom_set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collection.mtg_custom_set')),
            ],
        ),
    ]