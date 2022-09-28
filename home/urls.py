from django.urls import path, include
import home.views as hv

urlpatterns = [
    path('', hv.Index.as_view(), name='home_index'),
]