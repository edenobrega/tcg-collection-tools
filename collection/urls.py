from django.urls import path
import collection.views as cv

urlpatterns = [
    path('', cv.index.as_view(), name='collection_index'),
    path('mtg/', cv.mtg_index.as_view(), name='mtg_index'),
    path('mtg/sets', cv.mtg_set_list.as_view(), name='mtg_set_list'),
    path('mtg/view_set/<str:set_short>', cv.mtg_view_set.as_view(), name='mtg_view_set'),
    path('mtg/my_collection', cv.mtg_my_sets.as_view(), name='mtg_my_sets'),
    path('mtg/search', cv.mtg_search_cards.as_view(), name='mtg_search'),
    path('mtg/results', cv.mtg_search_results.as_view(), name='mtg_results'),
    path('mtg/custom/create', cv.mtg_create_custom_set.as_view(), name='mtg_custom_create'),
    path('mtg/custom/sets', cv.mtg_list_custom_sets.as_view(), name='mtg_custom_list'),
    path('mtg/custom/edit_collection/<int:id>', cv.mtg_edit_custom_set.as_view(), name='mtg_custom_edit'),
    path('mtg/search_json', cv.mtg_search_cards_json.as_view(), name='mtg_search_json'),
]