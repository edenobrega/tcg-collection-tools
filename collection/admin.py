from django.contrib import admin
from collection.models import mtg

# Register your models here.
admin.site.register(mtg.MTG_Card)
admin.site.register(mtg.MTG_Set)
admin.site.register(mtg.MTG_CardType)
admin.site.register(mtg.MTG_TypeLine)
admin.site.register(mtg.MTG_Collected)