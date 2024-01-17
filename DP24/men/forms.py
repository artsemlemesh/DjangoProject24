from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible

from .models import Category, Wife, Men


# @deconstructible
# class MikeValidator:
#     ALLOWED_CHARS = 'MIKEmike'
#     code = 'english' #name
#
#     def __init__(self, message=None):
#         self.message = message if message else 'only letters M I K E'
#
#     def __call__(self, value, *args, **kwargs): #when validator works out the method 'call' works out too/ we neet to redetermine it
#         if not (set(value) <= set(self.ALLOWED_CHARS)): # if at least one symbol in 'value' does not correspond to ALLOWED_CHARS it works out and throws an error below
#             raise ValidationError(self.message, code=self.code)



class AddPostForm(forms.ModelForm): # we used forms.Form, if using ModelForm then use Meta and some fields dont need anymore so we can comment them
    # title = forms.CharField(max_length=255, min_length=5,
    #                         label='Title',
    #                         widget=forms.TextInput(attrs={'class': 'form-input'}),
    #                         # validators=[
    #                         #     MikeValidator(),
    #                         # ]
    #                         error_messages={          #custom validation message, pops up if the field wasn't filled or wasn't filled correctly
    #                             'min_length': 'too short title',
    #                             'required': 'Title is compulsory'
    #                         }
    #                         )#label changes the name of the field on the page// widget attr customizes default class to input in our case
    # slug = forms.SlugField(max_length=255, label='URL',
    #                        validators=[ # create custom validators
    #                            MinLengthValidator(5, message='type minimum 5 symbols'), # we can also use validator in models, the same as here, just paste in the field as an attribute
    #                            MaxLengthValidator(50, message='100 symbols is a maximum')
    #                        ])
    # content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), required=False, label='Content') # adding required makes field to be optional to be filled// attrs customizes the size of the text field
    # is_published = forms.BooleanField(required=False,initial=True, label='Status')# in boolean fields initial=True selects empty box by default
    cat = forms.ModelChoiceField(queryset=Category.objects.all(),empty_label= 'not chosen', label='Categories') #empty_label, changes default -----  on what's in empty_label
    wife = forms.ModelChoiceField(queryset=Wife.objects.all(),empty_label= 'not married', required=False, label='Wife')

    class Meta:
        model = Men
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat', 'wife', 'tags']
        widgets = { #we need to redefine the widgets we wrote earlier, because we commented those fields above
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }
        labels = {'slug': 'URL'} # changes label from defauld slug to a new one ( also did before, but the field is commented) / we can write any name of the field in key and the new in value

    # after defining class Meta we can also use out validators: clean_title
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('length exceeds 50 characters')
        return title

    # def clean_title(self): #analogy of a MikeValidator(then we don't use attr validate in field), this is more convenient for local checks if we need to check one field (unlike MikeValidator for common and multiple usage)
    #     title = self.cleaned_data['title']
    #     ALLOWED_CHARS = 'MIKEmike'
    #
    #     if not (set(title) <= set(ALLOWED_CHARS)): # if at least one symbol in 'title' does not correspond to ALLOWED_CHARS it works out and throws an error below
    #         raise ValidationError('use only letters from ALLOWED_CHARS')

class UploadFileForm(forms.Form): #class not connected to a model
    file = forms.ImageField(label='FILE') # can be FileField(files and images) and ImageField(imagefield), for the latter we need to install package Pillow