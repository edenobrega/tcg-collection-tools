from django.shortcuts import render
from django.views import View


class Index(View):
    def get(self, request):
        print('Home index')
        return render(request, 'home/index.html')