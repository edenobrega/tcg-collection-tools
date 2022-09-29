from django.contrib import admin
from collection.models import mtg

# Register your models here.
admin.site.register(mtg.Card)
admin.site.register(mtg.Set)
admin.site.register(mtg.CardType)
admin.site.register(mtg.TypeLine)
admin.site.register(mtg.MTGCollected)