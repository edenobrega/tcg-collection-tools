from django.shortcuts import render
from django.views import View
from collection.models import mtg

# Create your views here.
class index(View):
    def get(self, request):
        mtg.Set.Update()