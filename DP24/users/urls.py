from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetDoneView, \
    PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, reverse_lazy
from . import views
from .views import RegisterUser



app_name = 'users'
urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'), # didnt use LogoutView because it wouldnt work for some reason

    path('password-change/', views.UserPasswordChange.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password_change_done'),#name should be exactly the same, because it is default success_url redirect for PasswordChangeView
#for PasswordChangeDoneView we defined our own html template and wrote it here in brackets, because it is the only change and there is no need to redefine the whole class for this purpose

    path('password-reset/', PasswordResetView.as_view(template_name='users/password_reset_form.html',
                                                      email_template_name='users/password_reset_email.html',
                                                      success_url=reverse_lazy('users:password_reset_done')), name='password_reset'),#we created these two urls for orchestrating pass reset
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),#the views are built-in, but templates are our own, slightly customized, url names should be exactly the same
    path('password-reset/<uidb64>/<token>', PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html',
                                                                             success_url=reverse_lazy('users:password_reset_complete')),name='password_reset_confirm'),
    path('password-reset/complete/',PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),name='password_reset_complete'),

    path('register/', RegisterUser.as_view(), name='register'),
    path('profile/', views.ProfileUser.as_view(), name='profile'),#not to see other users data we removed <int:pk>

]

