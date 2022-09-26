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
        data = list(mtg.Set.objects.all().values())

        return render(
            request,
            'mtg/sets.html',
            {
                'data': data
            }
        )


class mtg_view_set(View):
    def get(self, request, set_code):
        pass

    def post(self, request, set_code):
        pass
