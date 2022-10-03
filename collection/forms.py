from pickle import FALSE
from django import forms
from pkg_resources import require
from collection.models.mtg import Set, CardType

class MTGSearchForm(forms.Form):
    name = forms.CharField(max_length=200, required=False)
    converted_cost = forms.CharField(max_length=6, required=False)
    card_set = forms.ModelChoiceField(queryset=Set.objects.all(), required=False)
    types_select = forms.ModelChoiceField(queryset=CardType.objects.all(), required=False)
    types = forms.CharField(max_length=500, required=False)
    power = forms.CharField(max_length=3, required=False)
    toughness = forms.CharField(max_length=3, required=False)
