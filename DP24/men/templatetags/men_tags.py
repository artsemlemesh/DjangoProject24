from django import template
import men.views as views
from men.models import Category, TagPost
from django.db.models import Count
register = template.Library()

# @register.simple_tag(name='getcats')
# def get_categories():
#     return views.cats_db

@register.inclusion_tag('list_categories.html')# this tag is to mark a category a selected person belongs to( category turns blue)
def show_categories(cat_selected=0):
    cats = Category.objects.annotate(total=Count('posts')).filter(total__gt=0)
    return {'cats': cats, 'cat_selected': cat_selected}

@register.inclusion_tag('list_tags.html')
def show_all_tags():
    return {'tags': TagPost.objects.annotate(total=Count('tags')).filter(total__gt=0)}