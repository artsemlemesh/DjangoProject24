from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
from .views import RegisterUser

app_name = 'users'
urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'), # didnt use LogoutView because it wouldnt work for some reason
    path('register/', RegisterUser.as_view(), name='register'),
    path('profile/', views.ProfileUser.as_view(), name='profile'),#not to see other users data we removed <int:pk>

]

