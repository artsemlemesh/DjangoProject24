import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm


class LoginUserForm(AuthenticationForm): #inherited not from standart: forms.Form but from AuthenticationForm in order to use our own form: LoginUserFrom with functions of AuthenticationForm
    username = forms.CharField(label='login',
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='password',
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:#this form works with model user, thats why we write meta class, if user changes then we will get the new user automatically
        model = get_user_model()#returns model of user, it can change in the future, and in order not to change the code, we wrote it this way
        fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):#UserCreationForm replaced form.ModelForm. the latter is for manually created form, the former is for automated
    username = forms.CharField(label='login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='repeat password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta: #because the form is connected with the model we need to define class Meta
        model = get_user_model() #returns current user model
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'email': 'e-mail',
        }
        widgets = { #attribute widgets allows us to wtite syles(widgets) to a certain fields/ above we already did it for username, password1 and 2, here for email
            'email': forms.TextInput(attrs={ 'class': 'form-input'}),
        }

    #UserCreationForm does this check, so we comment it, it only needs for form.ModelForm
    # def clean_password2(self): #checks whether two passwords coinside
    #     cd = self.cleaned_data #cleadned_data is a dictionary that contains validated(checked) fields
    #     if cd['password1'] != cd['password2']:
    #         raise forms.ValidationError('passwords aren\'t equal')
    #     return cd['password1']


    def clean_email(self):#checks uniqueness of an email a new user is trying to register
        email = self.cleaned_data['email'] #gets already checked email from the form
        if get_user_model().objects.filter(email=email).exists():#checks whether it is in db
            raise forms.ValidationError('email already exists')#error if yes
        return email#if it is unique then returns it


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(disabled=True, label='email', widget=forms.TextInput(attrs={'class': 'form-input'}))
    #two fields below are for widgets: data_birth(defined with a new User class)
    this_year = datetime.date.today().year
    data_birth = forms.DateField(widget=forms.SelectDateWidget(years=tuple(range(this_year-100, this_year-5))))


    class Meta:  # because the form is connected with the model we need to define class Meta
        model = get_user_model()  # returns current user model
        fields = ['photo', 'username', 'data_birth', 'email']#add fields: photo and data_birth, we defined them with our new User class
        #since we dont have other fields we dont need to define labels and widgets, if we had some extra fields we would have writtent them there
        # labels = {
        #     'email': 'e-mail',
        # }
        # widgets = {
        #     # attribute widgets allows us to wtite syles(widgets) to a certain fields/ above we already did it for username, password1 and 2, here for email
        #     'email': forms.TextInput(attrs={'class': 'form-input'}),
        # }

#so we took those fields from PasswordChangeForm and SetPasswordForm and rewrote them slightly
class UserPasswordChangeForm(PasswordChangeForm): #PasswordChangeForm is a built in class, so we just inherit from it
    old_password = forms.CharField(label="Old password", widget=forms.PasswordInput(attrs={"class": "form-input"}))
    new_password1 = forms.CharField(label="New password", widget=forms.PasswordInput(attrs={"class": "form-input"}))
    new_password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput(attrs={"class": "form-input"}))

