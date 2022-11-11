from email.policy import default
from pickle import FALSE
from django import forms
from pkg_resources import require
from collection.models.mtg import MTG_Set, MTG_CardType

class MTGSearchForm(forms.Form):
    name = forms.CharField(max_length=200, required=False)
    converted_cost = forms.CharField(max_length=6, required=False)
    types_select = forms.ModelChoiceField(queryset=MTG_CardType.objects.all(), required=False)
    types = forms.CharField(max_length=500, required=False)
    power = forms.CharField(max_length=3, required=False)
    toughness = forms.CharField(max_length=3, required=False)
    search_collection = forms.BooleanField(initial=False, required=False)


class MTGCreateCustomSetForm(forms.Form):
    title = forms.CharField(min_length=1, max_length=200)
    description = forms.CharField(max_length=2000)
