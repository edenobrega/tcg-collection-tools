from django.urls import path
import collection.views as cv

urlpatterns = [
    path('', cv.index.as_view(), name='collection_index'),
    path('mtg/', cv.mtg_index.as_view(), name='mtg_index'),
    path('mtg/sets', cv.mtg_set_list.as_view(), name='mtg_set_list'),
    path('mtg/view_set', cv.mtg_view_set.as_view(), name='mtg_view_set'),
]