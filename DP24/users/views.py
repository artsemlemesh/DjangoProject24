from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from users.forms import LoginUserForm


def login_user(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data# cleaned_data is a dictionary containing the validated and cleaned data from the form fields
            user = authenticate(request, username=cd['username'],#if the form is valid, authenticates user
                                password=cd['password'])
            if user and user.is_active:#if the user is authenticated and active(not banned for example) then logs in the user
                login(request, user)#logs in the user
                return HttpResponseRedirect(reverse('index'))
    else:
        form = LoginUserForm()
    return render(request, 'users/login.html', {'form': form})

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))