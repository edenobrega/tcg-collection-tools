import json
from django.shortcuts import render, redirect
from django.views import View
from collection.models import mtg


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

        return render(
            request,
            'mtg/sets.html',
            {
                'data': data
            }
        )
