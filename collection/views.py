import json
from django.shortcuts import render, redirect
from django.views import View
from collection.models import mtg
from collection.forms import MTGSearchForm
from difflib import SequenceMatcher
from django.db.models import Q


def similar(a, b):
    if a.lower() in b.lower() or b.lower() in a.lower():
        return 1
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


class index(View):
    def get(self, request):
        return render(
            request,
            'index.html',
            {

            }
        )


class mtg_index(View):
    def get(self, request):
        return render(
            request,
            'mtg/index.html',
            {
                
            }
        )


class mtg_set_list(View):
    def get(self, request):
        _data = list(mtg.Set.objects.all().values())
        data = [{'name':x['name'], 'shorthand':x['shorthand'], 'set_type':mtg.SetType.objects.filter(id=x['set_type_id']).first().name, 'icon':x['icon']} for x in _data]
        return render(
            request,
            'mtg/sets.html',
            {
                'data': data
            }
        )


class mtg_view_set(View):
    def get(self, request, set_short):
        _temp = mtg.Set.objects.filter(shorthand=set_short).first()
        set_name = _temp.name
        shorthand = _temp.shorthand

        _data = list(mtg.Card.objects.filter(card_set__shorthand=set_short).values())
        data = []
        for d in _data:
            for u in d:
                if u == 'rarity_id':
                    d[u] = mtg.Rarity.objects.filter(id=d[u]).first().name.capitalize()
                if d[u] == None:
                    # None cannot be used in tabulator
                    d[u] = ''
            _temp = d

            # Add readable type line to dict
            type_line_str = ''
            type_line = mtg.TypeLine.objects.filter(card__id=d['id'])
            for tl in type_line:
                type_line_str = type_line_str + tl.type.name.lower().capitalize() + ' '
            _temp['type_line'] = type_line_str.strip()

            # Add collected count to dict
            collected = mtg.MTGCollected.objects.filter(owner=request.user, card__id=d['id'])
            if collected.exists():
                collected = collected.first()
                _temp['normal'] = collected.normal
                _temp['foil'] = collected.foil
            else:
                _temp['normal'] = 0
                _temp['foil'] = 0

            data.append(_temp)                
        return render(
            request,
            'mtg/view_set.html',
            {
                'card_set':set_name,
                'data': data,
                'shorthand': shorthand
            }
        )

    def post(self, request, set_short):
        data = json.loads(request.POST.get('Data'))
        for d in data:
            card = mtg.Card.objects.filter(
                        id=d['id'],
                        card_set__id=d['card_set_id'],
                        collector_number=d['collector_number']
                    ).first()

            collection_item = mtg.MTGCollected.objects.filter(
                owner = request.user,
                card = card
            )

            if not collection_item.exists() and (d['foil'] > 0 or d['normal'] > 0):
                collection_item = mtg.MTGCollected()
                collection_item.owner = request.user
                collection_item.card = card
                collection_item.normal = d['normal']
                collection_item.foil = d['foil']
                collection_item.save()
            elif d['foil'] > 0 or d['normal'] > 0:
                collection_item = collection_item.first()
                collection_item.normal = d['normal']
                collection_item.foil = d['foil']
                collection_item.save()
            elif collection_item.exists() and (d['foil'] == 0 or d['normal'] == 0):
                collection_item.delete()

        return redirect('mtg_view_set', set_short=set_short)


class mtg_my_sets(View):
    def get(self, request):
        shorts = mtg.MTGCollected.objects.filter(owner=request.user)
        # Get all unique set codes from above
        # TODO: Probably a better way to do this in one line
        shorts = list(set([s.card.card_set.shorthand for s in shorts]))

        _data = list(mtg.Set.objects.filter(shorthand__in=shorts).values())
        data = [{'name':x['name'], 'shorthand':x['shorthand'], 'set_type':mtg.SetType.objects.filter(id=x['set_type_id']).first().name, 'icon':x['icon']} for x in _data]

        for d in data:
            card_count = mtg.Card.objects.filter(card_set__shorthand=d['shorthand']).__len__()
            d['card_count'] = card_count
            collected_cards = mtg.MTGCollected.objects.filter(owner=request.user, card__card_set__shorthand=d['shorthand'])
            d['single_card_collected_normal'] = len(collected_cards.filter(normal__gte=1))
            d['set_collected_normal'] = len(collected_cards.filter(normal__gte=4))

        return render(
            request,
            'mtg/collection_sets.html',
            {
                'data': data
            }
        )


class mtg_search_cards(View):
    def get(self, request):
        form = MTGSearchForm()
        return render(
            request,
            'mtg/search_cards.html',
            {
                'form':form
            }
        )


class mtg_search_results(View):
    # TODO: large searches are very slow, instead of loading all should perhaps load it into pages and serve one at a time, or just find a faster way to filter
    def get(self, request):
        cards = []
        query = Q()
        name_ = request.GET['name']
        converted_cost_ = request.GET['converted_cost']
        card_set_ = request.GET['card_set']
        types_ = request.GET['types']
        power_ = request.GET['power']
        toughness_ = request.GET['toughness']

        if name_:
            query &= Q(name=name_)
        if converted_cost_:
            query &= Q(converted_cost=converted_cost_)
        if card_set_:
            query &= Q(card_set__id=card_set_)
        if power_:
            query &= Q(power=power_)
        if toughness_:
            query &= Q(toughness=toughness_)

        # TODO: filter first if has creature,enhancement,instant,sorcery,planeswalker

        if query != Q():
            cards = list(mtg.Card.objects.filter(query))

        if types_:
            types = request.GET['types'].split(',')
            if '—' in types:
                types.remove('—')
            if '//' in types:
                types.remove('//')
            if '' in types:
                types.remove('')

            types_set = set(types)     
           
            if cards == []:
                type_ = mtg.CardType.objects.filter(name=types[-1])
                # list of those that have atleast one of asked for type
                typeline = mtg.TypeLine.objects.filter(type=type_.first())

                for tl in typeline:
                    ctypes = mtg.TypeLine.objects.exclude(type__id__in=[2,50]).filter(card=tl.card)
                    if len(ctypes) < len(types):
                        continue
                    type_line_list = [x.type.name for x in ctypes]
                    if types_set.issubset(set(type_line_list)):
                        cards.append(tl.card)
            else:
                cards_ = list(cards)
                cards = []
                for c in cards_:
                    ctypes = mtg.TypeLine.objects.exclude(type__id__in=[2,50]).filter(card=c)
                    if len(ctypes) < len(types):
                        continue
                    type_line_list = [x.type.name for x in ctypes]
                    if types_set.issubset(set(type_line_list)):
                        cards.append(c)

        
        data = []
        # TODO: should return the set of eachcard instead of collector number, thats useless when cards from multiple sets are mixed together        
        for c in cards:
            card_dict = {}
            card_dict['collector_number'] = c.collector_number 
            card_dict['name'] = c.name
            card_dict['text'] =  c.text or ''
            card_dict['flavor'] = c.flavor or ''
            card_dict['rarity_id'] = c.rarity.name.capitalize()

            type_line_str = ''
            type_line = mtg.TypeLine.objects.filter(card=c)
            for tl in type_line:
                type_line_str = type_line_str + tl.type.name.lower().capitalize() + ' '
            card_dict['type_line'] = type_line_str.strip()
            
            collected = mtg.MTGCollected.objects.filter(owner=request.user, card=c)
            if collected.exists():
                card_dict['normal'] = collected.first().normal
                card_dict['foil'] = collected.first().foil
            else:
                card_dict['normal'] = 0
                card_dict['foil'] = 0
            data.append(card_dict)

        return render(
            request,
            'mtg/view_set.html',
            {
                'card_set':'Custom Search',
                'data': data,
                'shorthand': 'n/a'
            }
        )
