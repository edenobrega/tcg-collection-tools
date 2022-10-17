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
    icon = models.URLField(max_length=300)
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
    mana_cost = models.CharField(max_length=50)
    converted_cost = models.IntegerField(null=True)  
    text = models.CharField(max_length=1000, null=True)
    flavor = models.CharField(max_length=1000, null=True)
    artist = models.CharField(max_length=100)
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

# TODO: Replace exists > else with a different implementation that does not require the else
def Update():
    from django.conf import settings
    if not settings.UPDATE_MTG:
        return    

    import time

    if settings.UPDATE_FROM_API:
        print('Requesting bulkdata list')
        bulk = requests.get('https://api.scryfall.com/bulk-data')

        # Search for uri of bulk .json of all cards
        obj = next(x['download_uri'] for x in bulk.json()['data'] if x['type'] == 'default_cards')

        print('Requesting default_cards bulk file')
        # Get the .json
        req = requests.get(obj)

        js = req.json()
    else:
        try:
            print('opening file')
            fi = open(settings.MTG_FILE_LOCATION, encoding='utf8')
            print('file open')
            import json
            print('loading json')
            js = json.load(fi)
            print('json loaded')
        except Exception as e:
            print(e)
            print('loading from file failed')
            return

    for _card in js:
        if 'oracle_id' in _card:
            # Check if card already exists
            exist = MTG_Card.objects.filter(
                name=_card['name'],
                oracle_id=_card['oracle_id'],
                card_set__shorthand=_card['set'],
                collector_number=_card['collector_number']
            )
        else:
            exist = MTG_Card.objects.filter(
                name=_card['name'],
                oracle_id=_card['card_faces'][0]['oracle_id'],
                card_set__shorthand=_card['set'],
                collector_number=_card['collector_number']
            )

        if exist.exists():
            exist = exist.first()
            print(f'MTG_Card: {exist.name} of set: {exist.card_set.name} Exists')
            continue

        # Check if set is in db, and update if not
        card_set = MTG_Set.objects.filter(
            shorthand=_card['set']
        )

        set_type = MTG_SetType.objects.filter(
            name=_card['set_type']
        )

        if not set_type.exists():
            _temp = _card['set_type']
            print(f'MTG_Set Type {_temp} does not exist, creating')
            set_type = MTG_SetType()
            set_type.name = _card['set_type']
            set_type.save()
        else:
            set_type = set_type.first()

        if not card_set.exists():
            _temp = _card['set_name'] + '|' + _card['set']
            print(f'MTG_Set {_temp} does not exist, creating')
            card_set = MTG_Set()
            card_set.name = _card['set_name']
            card_set.shorthand = _card['set']
            card_set.search_uri = _card['set_uri']          
            time.sleep(0.150)
            # Make request to get set as it holds the icon svg
            _req = requests.get(_card['set_uri'])
            if _req.status_code == '200':
                card_set.icon = _req.json()['icon_svg_uri']
            
            card_set.set_type = set_type
            card_set.save()
        else:
            card_set = card_set.first()

        card = MTG_Card()
        card.name = _card['name']
        card.card_set = card_set
        if 'mana_cost' in _card:
            card.mana_cost = _card['mana_cost']
        if 'cmc' in _card:
            card.converted_cost = _card['cmc']
        if 'oracle_text' in _card:
            card.text = _card['oracle_text']
        if 'flavor_text' in _card:
            card.flavor = _card['flavor_text']
        # will always have a artist but no harm in checking
        if 'artist' in _card:
            card.artist = _card['artist']
        if 'collector_number' in _card:
            card.collector_number = _card['collector_number']
        if 'power' in _card:
            card.power = _card['power']
        if 'toughness' in _card:
            card.toughness = _card['toughness']
        if 'image_uris' in _card:
            card.image = _card['image_uris']['normal']
        elif 'card_faces' in _card:
            if 'image_uris' in _card['card_faces'][0]:
                card.image = _card['card_faces'][0]['image_uris']['normal']
                card.image_flipped = _card['card_faces'][1]['image_uris']['normal']

        card.scryfall_id = _card['id']
        if 'oracle_id' in _card:
            card.oracle_id = _card['oracle_id']
        else:
            card.oracle_id = _card['card_faces'][0]['oracle_id']

        _rarity = MTG_Rarity.objects.filter(name=_card['rarity'])
        if not _rarity.exists():
            _temp = _card['rarity']
            print(f'MTG_Rarity {_temp} does not exist, creating')
            _rarity = MTG_Rarity()
            _rarity.name = _card['rarity']
            _rarity.save()
        else:
            _rarity = _rarity.first()

        card.rarity = _rarity
        card.save()
        if 'type_line' in _card:
            _types = [u.upper() for u in _card['type_line'].replace('-', '').split(' ') if u != '']
        else:
            _types = [u.upper() for u in _card['card_faces'][0]['type_line'].replace('-', '').split(' ') if u != '']
        for ct in _types:
            cardtype = MTG_CardType.objects.filter(name=ct)
            if not cardtype.exists():
                print(f'MTG_Card Type {ct} does not exist, creating')
                cardtype = MTG_CardType()
                cardtype.name = ct
                cardtype.save()
            else:
                cardtype = cardtype.first()
            typeline = MTG_TypeLine()
            typeline.card = card
            typeline.type = cardtype
            typeline.save()


