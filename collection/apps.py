from django.apps import AppConfig


class CollectionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'collection'

    def ready(self):
        from .models import mtg
        import sys
        if 'runserver' in sys.argv:
            print('Updating MTG data')
            mtg.Set.Update()
            mtg.Card.Update()