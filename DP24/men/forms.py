from django import forms
from .models import Category, Wife



class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255)
    slug = forms.SlugField(max_length=255)
    content = forms.CharField(widget=forms.Textarea(), required=False) # adding required makes field to be optional to be filled
    is_published = forms.BooleanField(required=False)
    cat = forms.ModelChoiceField(queryset=Category.objects.all())
    wife = forms.ModelChoiceField(queryset=Wife.objects.all(), required=False)
