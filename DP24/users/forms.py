from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm


class LoginUserForm(AuthenticationForm): #inherited not from standart: forms.Form but from AuthenticationForm in order to use our own form: LoginUserFrom with functions of AuthenticationForm
    username = forms.CharField(label='login',
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='password',
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:#this form works with model user, thats why we write meta class, if user changes then we will get the new user automatically
        model = get_user_model()#returns model of user, it can change in the future, and in order not to change the code, we wrote it this way
        fields = ['username', 'password']


class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(label='login')
    password = forms.CharField(label='password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='repeat password', widget=forms.PasswordInput())

    class Meta: #because the form is connected with the model we need to define class Meta
        model = get_user_model() #returns current user model
        fields = ['username', 'email', 'password', 'password2']
        labels = {
            'email': 'e-mail',
        }