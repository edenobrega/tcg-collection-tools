from django.contrib.auth.models import User
from django.db import models
import requests


class MTG_Rarity(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name}'


class MTG_SetType(models.Model):
    name = models.CharField(max_length=50)


class MTG_Set(models.Model):
    name = models.CharField(max_length=100)
    shorthand = models.CharField(max_length=20)
    icon = models.URLField(max_length=300, null=True)
    search_uri = models.URLField(max_length=500)
    set_type = models.ForeignKey(MTG_SetType, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.shorthand} - {self.name}'


class MTG_CardType(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return f'{self.name}'


# W = White
# U = Blue
# B = Black
# R = Red
# G = Green
class MTG_Card(models.Model):
    name = models.CharField(max_length=200)
    card_set = models.ForeignKey(MTG_Set, on_delete=models.CASCADE, blank=False, null=False)
    mana_cost = models.CharField(max_length=50, null=True)
    converted_cost = models.IntegerField(null=True)  
    text = models.CharField(max_length=1000, null=True)
    flavor = models.CharField(max_length=1000, null=True)
    artist = models.CharField(max_length=100, null=True)
    collector_number = models.CharField(max_length=25, null=False)
    power = models.CharField(max_length=10, null=True)
    toughness = models.CharField(max_length=10, null=True)
    scryfall_id = models.CharField(max_length=36)
    oracle_id = models.CharField(max_length=36)

    rarity = models.ForeignKey(MTG_Rarity, on_delete=models.CASCADE)
    # image will be face, flipped will be back
    image = models.URLField(null=True)
    image_flipped = models.URLField(null=True)

    def __str__(self):
        return f'{self.name} - {self.card_set.shorthand} - {self.collector_number}'


class MTG_TypeLine(models.Model):
    type = models.ForeignKey(MTG_CardType, on_delete=models.CASCADE, blank=False, null=False)
    card = models.ForeignKey(MTG_Card, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return f'{self.card.name} - {self.type.name}'


class MTG_Collected(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(MTG_Card, on_delete=models.CASCADE)
    normal = models.IntegerField()
    foil = models.IntegerField()

    def __str__(self):
        return f'{self.owner} | {self.card.name} | {self.card.card_set.shorthand} | {self.normal} | {self.foil}'


class MTG_Custom_Set(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=False)
    description = models.TextField(max_length=2000, null=False)


class MTG_Custom_Set_Cards(models.Model):
    custom_set = models.ForeignKey(MTG_Custom_Set, on_delete=models.CASCADE)
    card = models.ForeignKey(MTG_Card, on_delete=models.CASCADE)
    normal = models.IntegerField()
    foil = models.IntegerField()
