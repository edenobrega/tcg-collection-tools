from email.mime import image
import json
from operator import truediv
from tabnanny import check
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
# TODO: Add converted manacost
class Card(models.Model):
    name = models.CharField(max_length=200)
    card_set = models.ForeignKey(Set, on_delete=models.CASCADE, blank=False, null=False)
    mana_cost = models.CharField(max_length=20)
    text = models.CharField(max_length=500, null=True)
    flavor = models.CharField(max_length=500, null=True)
    artist = models.CharField(max_length=100)
    collector_number = models.CharField(max_length=6, null=False)
    power = models.CharField(max_length=3, null=True)
    toughness = models.CharField(max_length=3, null=True)
    scryfall_id = models.CharField(max_length=36)
    converted_cost = models.IntegerField(null=True)
    # image will be face, flipped will be back
    image = models.URLField(null=True)
    image_flipped = models.URLField(null=True)

    def Update():
        # Below is for updating cards via file dump
        # f = 'UNIQUE ARTWORK DUMP FROM SCRYFALL HERE' 
        # fi = open(f+'.json', encoding='utf8') 
        # j = json.load(fi)
        # print(len(Card.objects.filter(image=None)))
        # for c in Card.objects.filter(image=None):
        #     try:
        #         obj = next(x for x in j if x['id'] == c.scryfall_id)
        #     except:
        #         continue
        #     if 'image_uris' in obj:
        #         c.image = obj['image_uris']['normal']
        #     elif 'card_faces' in obj:
        #         c.image = obj['card_faces'][0]['image_uris']['normal']
        #         c.image_flipped = obj['card_faces'][1]['image_uris']['normal']
        #     else:
        #         continue
        #     c.save()
        # print(len(Card.objects.filter(image=None)))
        # return
        import time     

        sets = Set.objects.all()

        for _set in sets:
            r = requests.get(_set.search_uri)
            _json = r.json()
            current_count = len(Card.objects.filter(card_set=_set))
            cc = _json['card_count']
            if current_count != cc:
                print(f'{_set.name} is missing {cc-current_count} card/s')
                print('Adding cards')
                s_uri = _json['search_uri']
                print(f'Making request to {s_uri}')
                r = requests.get(_json['search_uri'])
                print(r.status_code)
                if r.status_code != 200:
                    continue           
                while True:
                    cl_json = r.json()

                    for d in cl_json['data']:
                        if Card.objects.filter(scryfall_id=d['id']).exists():
                            temp_name = d['name']
                            temp_collectors = d['collector_number']
                            print(f'Card {temp_name}, {temp_collectors}, of set {_set.shorthand} exists already')
                            continue

                        new_card = Card()

                        new_card.name = d['name']
                        new_card.card_set = _set
                        if 'mana_cost' in d:
                            new_card.mana_cost = d['mana_cost']
                        if 'oracle_text' in d:
                            new_card.text = d['oracle_text']
                        if 'flavor_text' in d:
                            new_card.flavor = d['flavor_text']
                        new_card.artist = d['artist']
                        new_card.collector_number = d['collector_number']
                        if 'power' in d:
                            new_card.power = d['power']
                        if 'toughness' in d:
                            new_card.toughness = d['toughness']
                        new_card.scryfall_id = d['id']

                        if 'image_uris' in _json:
                            c.image = _json['image_uris']['normal']
                        elif 'card_faces' in _json:
                            c.image = _json['card_faces'][0]['image_uris']['normal']
                            c.image_flipped = _json['card_faces'][1]['image_uris']['normal']
                        else:
                            print('Error: No images found for card')

                        new_card.save()

                    if not cl_json['has_more']:
                        print(f'Finished Updating {_set.name}')
                        break
                    time.sleep(0.150)
                    r = requests.get(cl_json['next_page'])


class TypeLine(models.Model):
    type = models.ForeignKey(Type, on_delete=models.CASCADE, blank=False, null=False)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, blank=False, null=False)