from operator import truediv
from django.db import models
import requests

class Set(models.Model):
    name = models.CharField(max_length=100)
    shorthand = models.CharField(max_length=20)
    icon = models.URLField(max_length=300)
    search_uri = models.URLField(max_length=500)
    set_type = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.shorthand} - {self.name}'

    def Update():
        r = requests.get('https://api.scryfall.com/sets')
        if r.status_code != 200:
            return

        for d in r.json()['data']:
            if d['object'] == 'set' and Set.objects.filter(name=d['name']).exists():
                continue
            new_set = Set()
            new_set.name = d['name']
            new_set.shorthand = d['code']
            new_set.icon = d['icon_svg_uri']
            new_set.search_uri = d['uri']
            new_set.set_type = d['set_type']
            new_set.save()


class Type(models.Model):
    name = models.CharField(max_length=300)


# W = White
# U = Blue
# B = Black
# R = Red
# G = Green
class Card(models.Model):
    name = models.CharField(max_length=200)
    card_set = models.ForeignKey(Set, on_delete=models.CASCADE, blank=False, null=False)
    mana_cost = models.CharField(max_length=20)
    text = models.CharField(max_length=500)
    flavor = models.CharField(max_length=500)
    artist = models.CharField(max_length=100)
    collector_number = models.IntegerField(null=False)
    power = models.CharField(max_length=3)
    toughness = models.CharField(max_length=3)

    def update_cards():
        pass


class TypeLine(models.Model):
    type = models.ForeignKey(Type, on_delete=models.CASCADE, blank=False, null=False)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, blank=False, null=False)