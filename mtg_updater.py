import time
import requests
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, literal
from sqlalchemy.orm import Session

base = automap_base()
engine = create_engine('mssql+pyodbc://DESKTOP-80083JA\\SQLEXPRESS/tcgct_bravo?driver=ODBC+Driver+17+for+SQL+Server')
base.prepare(engine, reflect=True)

# Tables
Card = base.classes.collection_mtg_card
CardType = base.classes.collection_mtg_cardtype
Collected = base.classes.collection_mtg_collected
Rarity = base.classes.collection_mtg_rarity
Set = base.classes.collection_mtg_set
SetType = base.classes.collection_mtg_settype
TypeLine = base.classes.collection_mtg_typeline


session = Session(engine)
session.autocommit = True


bulk = requests.get('https://api.scryfall.com/bulk-data')

# Search for uri of bulk .json of all cards
obj = next(x['download_uri'] for x in bulk.json()['data'] if x['type'] == 'default_cards')

print('Requesting default_cards bulk file')
# Get the .json
req = requests.get(obj)

js = req.json()

for _card in js:
    # Check if card already exists
    q = session.query(Card).filter_by(
        scryfall_id=_card['id']          
    ).first()

    if q:
        continue

    # Check if set is in db, and update if not
    card_set = session.query(Set).filter_by(shorthand=_card['set']).first()

    set_type = session.query(SetType).filter_by(name=_card['set_type']).first()

    if not set_type:
        _temp = _card['set_type']
        set_type = SetType(name=_card['set_type'])
        session.add(set_type)
        session.flush()

    if not card_set:
        _temp = _card['set_name'] + '|' + _card['set']

        card_set = Set(
            name=_card['set_name'],
            shorthand = _card['set'],
            search_uri = _card['set_uri'],
            set_type_id = set_type.id
        )

        time.sleep(0.150)
        # Make request to get set as it holds the icon svg
        _req = requests.get(_card['set_uri'])
        if _req.status_code == '200':
            card_set.icon = _req.json()['icon_svg_uri']
        session.add(card_set)
        session.flush()


    card = Card()
    card.name = _card['name']
    card.card_set_id = card_set.id
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

    _rarity = session.query(Rarity).filter_by(name=_card['rarity']).first()
    if not _rarity:
        _temp = _card['rarity']
        _rarity = Rarity()
        _rarity.name = _card['rarity']
        session.add(_rarity)
        session.flush()

    card.rarity_id = _rarity.id
    session.add(card)
    session.flush()

    if 'type_line' in _card:
        _types = [u.upper() for u in _card['type_line'].replace('-', '').split(' ') if u != '']
    else:
        _types = [u.upper() for u in _card['card_faces'][0]['type_line'].replace('-', '').split(' ') if u != '']
    for ct in _types:
        cardtype = session.query(CardType).filter_by(name=ct).first()
        if not cardtype:
            cardtype = CardType()
            cardtype.name = ct
            session.add(cardtype)
            session.flush()

        typeline = TypeLine()
        typeline.card_id = card.id
        typeline.type_id = cardtype.id
        session.add(typeline)
        session.flush()
