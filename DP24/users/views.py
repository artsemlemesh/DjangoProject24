from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy

from users.forms import LoginUserForm, RegisterUserForm


class LoginUser(LoginView):
    form_class = LoginUserForm #built in class AuthenticationForm was replaced by our form that inherits functions of a AuthenticationForm
    template_name = 'users/login.html'
    extra_context = {'title': 'authorization'}

    def get_success_url(self):# had to rewrite, because LoginView class redirected us to a wrong page initially
        return reverse_lazy('index')


def logout_user(request): #used built in LogoutView
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))


def register(request):
    if request.method == 'POST':   #if user submits the form
        form = RegisterUserForm(request.POST)#create form with data that user filled
        if form.is_valid():#if the data is correct
            user = form.save(commit=False)#dont yet save to the db
            user.set_password(form.cleaned_data['password'])#set_password encrypts our password and puts it in attribute 'password', in brackets we write which password we want to be encrypted (form.cleaned_data['password'])
            user.save()#save the user to the db
            return render(request, 'users/register_done.html')
    else:
        form = RegisterUserForm()

    return render(request, 'users/register.html', {'form': form})









# def login_user(request): # it has been replaced by built-in class based view (LoginView)
#     if request.method == 'POST':
#         form = LoginUserForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data# cleaned_data is a dictionary containing the validated and cleaned data from the form fields
#             user = authenticate(request, username=cd['username'],#if the form is valid, authenticates user
#                                 password=cd['password'])
#             if user and user.is_active:#if the user is authenticated and active(not banned for example) then logs in the user
#                 login(request, user)#logs in the user
#                 return HttpResponseRedirect(reverse('index'))
#     else:
#         form = LoginUserForm()
#     return render(request, 'users/login.html', {'form': form})
#
