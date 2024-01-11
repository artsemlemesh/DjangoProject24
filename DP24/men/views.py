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
    {'id': 1, 'title': 'Albert Einstein', 'content': '''<h3>14 March 1879 – 18 April 1955</h3> was a German-born theoretical physicist who is widely held to be one of the greatest and 
    most influential scientists of all time. Best known for developing the theory of relativity, Einstein also made important contributions to quantum mechanics, and was thus a central figure in the revolutionary reshaping of the scientific understanding of nature
     that modern physics accomplished in the first decades of the twentieth century.[1][5] His mass–energy equivalence formula E = mc2, which arises from relativity theory, has been called "the world's most famous equation".[6] He received the 1921 Nobel Prize in 
     Physics "for his services to theoretical physics, and especially for his discovery of the law of the photoelectric effect",[7] a pivotal step in the development of quantum theory. His work is also known for its influence on the philosophy of science.[8][9] 
    In a 1999 poll of 130 leading physicists worldwide by the British journal Physics World, Einstein was ranked the greatest physicist of all time.[10] His intellectual achievements and originality have made the word Einstein broadly synonymous with genius.[11]''', 'is_p': True},
    {'id': 2, 'title': 'Thomas Eddison', 'content': '''<h3>American inventor and businessman.</h3>[1][2][3] He developed many devices in fields such as electric power generation,
     mass communication, sound recording, and motion pictures.[4] These inventions, which include the phonograph, the motion picture camera, and early versions of the electric light bulb, have had a widespread impact on the modern industrialized world.[5] 
     He was one of the first inventors to apply the principles of organized science and teamwork to the process of invention, working with many researchers and employees.
     He established the first industrial research laboratory.[6]''', 'is_p': True},
    {'id': 3, 'title': 'Elon Mask', 'content': '''<h3>Businessman and investor.</h3> He is the founder, chairman, CEO, and CTO of SpaceX; angel investor, CEO, product architect and former chairman of Tesla, Inc.; owner, chairman and CTO of X Corp.;
     founder of the Boring Company and xAI; co-founder of Neuralink and OpenAI; and president of the Musk Foundation. He is the wealthiest person in the world, with an estimated net worth of US$232 billion as of December 2023, according to the Bloomberg Billionaires Index,
      and $254 billion according to Forbes,
     primarily from his ownership stakes in Tesla and SpaceX.[5][6]''', 'is_p': True},

]

cats_db = [
    {'id': 1, 'name': 'Actresses'},
    {'id': 2, 'name': 'Singers'},
    {'id': 3, 'name': 'Sportsmen'}
]


def index(request):
    context = {'title': 'main page',
               'menu': menu,
               'posts': data_db,
               'cat_selected': 0
               }
    return render(request, 'index.html', context) #render handles template and returns it to the client



def show_post(request, post_id):
    return HttpResponse(f'article with id: {post_id}')

def about(request):
    return render(request, 'about.html', {'title':'about', 'menu': menu})

def addpage(request):
    return HttpResponse('addpage')

def contact(request):
    return HttpResponse('contact')

def login(request):
    return HttpResponse('login')

def show_category(request, cat_id):
    context = {'title': 'main page',
               'menu': menu,
               'posts': data_db,
               'cat_selected': cat_id
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