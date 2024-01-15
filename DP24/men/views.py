from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse
from django.template.defaultfilters import slugify

from .forms import AddPostForm
from .models import Men, Category, TagPost

# Create your views here.


menu = [{'title': 'about us', 'url_name': 'about'},
        {'title': 'add article', 'url_name': 'add_page'},
        {'title': 'feedback', 'url_name': 'contact'},
        {'title': 'login', 'url_name': 'login'}
]




def index(request):
    posts = Men.published.all().select_related('cat') # Manager published returns only published posts
    context = {'title': 'main page',
               'menu': menu,
               'posts': posts,
               'cat_selected': 0
               }
    return render(request, 'index.html', context) #render handles template and returns it to the client



def show_post(request, post_slug):
    post = get_object_or_404(Men, slug=post_slug)

    context = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1

    }
    return render(request, 'post.html', context)

def about(request):
    return render(request, 'about.html', {'title':'about', 'menu': menu})

def addpage(request):
    form = AddPostForm()
    context = {
        'menu': menu,
        'title': 'add page',
        'form': form
    }
    return render(request, 'addpage.html', context)

def contact(request):
    return HttpResponse('contact')

def login(request):
    return HttpResponse('login')

def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug) # (first argument (Category)- choose model from which we need to get something, second argument (slug) is a criterion based on which we need to select posts/ slug = cat_slug
    posts = Men.published.filter(cat_id=category.pk).select_related('cat') # returns posts whose id equals slug we read above
# we use select_related('cat') in order to eliminate repetitive SQL requests, it optimises the website ()
    context = {'title': f'Category: {category.name}',
               'menu': menu,
               'posts': posts,
               'cat_selected': category.pk
               }
    return render(request, 'index.html', context)

# def categories(request, cat_id):
#     return HttpResponse(f'cats, id: {cat_id}')
#
# def categories_by_slug(request, cat_slug):
#     print(request.GET)
#     return HttpResponse(f'cats, slug: {cat_slug}')
#
# def archive(request, year):
#     if year > 2024:
#         return redirect(reverse('cats', args=('music', )))
#     return HttpResponse(f'archive by years: {year}')

#redirect and HttpResponseRedirect self replaceble, work the same way, but better to use redirect


def page_not_found(request, exception):     # connected to handler404 in urls.py
    return HttpResponseNotFound('<h1>PAGE NOT FOUND</h1>')

def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Men.Status.PUBLISHED).select_related('cat')
    context = {
        'title': f'Tag: {tag.tag}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None
    }

    return render(request, 'index.html', context)