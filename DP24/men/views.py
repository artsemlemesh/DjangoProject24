from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse
from django.template.defaultfilters import slugify

# Create your views here.


menu = [{'title': 'about us', 'url_name': 'about'},
        {'title': 'add article', 'url_name': 'add_page'},
        {'title': 'feedback', 'url_name': 'contact'},
        {'title': 'login', 'url_name': 'login'}
]
data_db = [
    {'id': 1, 'title': 'Albert Einstein', 'content': 'Memouir of Albert', 'is_p': True},
    {'id': 2, 'title': 'Thomas Eddison', 'content': 'Memouir of Thomas Eddison', 'is_p': False},
    {'id': 3, 'title': 'Elon Mask', 'content': 'Memouir of Elon Mask', 'is_p': True},

]

def index(request):
    context = {'title': 'main page',
               'menu': menu,
               'posts': data_db,
               }
    return render(request, 'index.html', context) #render handles template and returns it to the client



def show_post(request, post_id):
    return HttpResponse(f'article with id: {post_id}')

def about(request):
    return HttpResponse('about us')

def addpage(request):
    return HttpResponse('addpage')

def contact(request):
    return HttpResponse('contact')

def login(request):
    return HttpResponse('login')


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