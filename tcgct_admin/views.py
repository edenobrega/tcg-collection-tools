from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import UserCreationForm

class register_view(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'tcgct_admin/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home_index')
        return render(request, 'tcgct_admin/register.html', {'form': form})


class login_view(View):
    def get(self, request):
        return render(request, 'tcgct_admin/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home_index')
        else:
            return redirect('login_view')


def logout_view(request):
    logout(request)
    return redirect('home_index')
