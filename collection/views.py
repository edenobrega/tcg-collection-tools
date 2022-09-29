import json
from django.shortcuts import render
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
        data = [{'name':x['name'], 'shorthand':x['shorthand'], 'set_type':mtg.SetType.objects.filter(id=x['set_type_id']).first().name} for x in _data]
        return render(
            request,
            'mtg/sets.html',
            {
                'data': data
            }
        )


class mtg_view_set(View):
    def get(self, request, set_short):
        set_name = mtg.Set.objects.filter(shorthand=set_short).first().name

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

            type_line_str = ''
            type_line = mtg.TypeLine.objects.filter(card__id=d['id'])
            for tl in type_line:
                type_line_str = type_line_str + tl.type.name.lower().capitalize() + ' '
            _temp['type_line'] = type_line_str
            data.append(_temp)

        return render(
            request,
            'mtg/view_set.html',
            {
                'card_set':set_name,
                'data': data
            }
        )

    def post(self, request, set_short):
        pass
