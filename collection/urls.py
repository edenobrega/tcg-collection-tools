from django.urls import path
import collection.views as cv

urlpatterns = [
    path('', cv.index.as_view(), name='collection_index'),
]