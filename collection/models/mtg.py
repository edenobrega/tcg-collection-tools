from django.db import models
import requests


class Rarity(models.Model):
    name = models.CharField(max_length=20)


class SetType(models.Model):
    name = models.CharField(max_length=50)


class Set(models.Model):
    name = models.CharField(max_length=100)
    shorthand = models.CharField(max_length=20)
    icon = models.URLField(max_length=300)
    search_uri = models.URLField(max_length=500)
    set_type = models.ForeignKey(SetType)

    def __str__(self):
        return f'{self.shorthand} - {self.name}'


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
    converted_cost = models.IntegerField(null=True)  
    text = models.CharField(max_length=500, null=True)
    flavor = models.CharField(max_length=500, null=True)
    artist = models.CharField(max_length=100)
    collector_number = models.CharField(max_length=6, null=False)
    power = models.CharField(max_length=3, null=True)
    toughness = models.CharField(max_length=3, null=True)
    scryfall_id = models.CharField(max_length=36)
    oracle_id = models.CharField(max_length=36)

    rarity = models.ForeignKey(Rarity)
    # image will be face, flipped will be back
    image = models.URLField(null=True)
    image_flipped = models.URLField(null=True)


class TypeLine(models.Model):
    type = models.ForeignKey(Type, on_delete=models.CASCADE, blank=False, null=False)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, blank=False, null=False)


def Update():
    import time
    # f = 'UNIQUE ARTWORK DUMP FROM SCRYFALL HERE' 
    # fi = open(f+'.json', encoding='utf8') 
    # j = json.load(fi)
    # Get list of bulkdata
    bulk = requests.get('https://api.scryfall.com/bulk-data')

    # Search for uri of bulk .json of all cards
    obj = next(x['download_uri'] for x in bulk.json()['data'] if x['type'] == 'default_cards')

    # Get the .json
    req = requests.get(obj)
    if req.status_code != '200':
        print(f'Request failed, Code:{req.status_code}')

    js = req.json()
    for _card in js:
        # Check if card already exists
        exist = Card.objects.filter(
            name=_card['name'],
            oracle_id=_card['oracle_id'],
            card_set__shorthand=_card['set'],
            collector_number=_card['collector_number']
        ).exists()

        if exist:
            continue

        card_set = Set.objects.filter(
            shorthand=_card['set']
        )

        set_type = SetType.objects.filter(
            name=_card['set_type']
        )

        if not set_type.exists():
            set_type = SetType()
            set_type.name = _card['set_type']
            set_type.save()
        
        if not card_set.exists():
            card_set = Set()
            card_set.name = _card['set_name']
            card_set.shorthand = _card['set']
            card_set.search_uri = _card['set_uri']          
            time.sleep(0.150)
            _req = requests.get(_card['set_uri'])
            if _req.status_code == '200':
                card_set.icon = _req.json()['icon_svg_uri']
            card_set.set_type = set_type
            card_set.save()

            
