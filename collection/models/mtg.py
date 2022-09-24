from django.db import models

class Set(models.Model):
    name = models.CharField(max_length=100)
    shorthand = models.CharField(max_length=20)
    icon = models.URLField(max_length=300)


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


class TypeLine(models.Model):
    type = models.ForeignKey(Type, on_delete=models.CASCADE, blank=False, null=False)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, blank=False, null=False)