from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.views.generic import ListView, DetailView

from .forms import AddPostForm, UploadFileForm
from .models import Men, Category, TagPost, UploadFiles
from django.views import View
# Create your views here.


menu = [{'title': 'about us', 'url_name': 'about'},
        {'title': 'add article', 'url_name': 'add_page'},
        {'title': 'feedback', 'url_name': 'contact'},
        {'title': 'login', 'url_name': 'login'}
]




# def index(request): # replaced by MenHome
#     posts = Men.published.all().select_related('cat') # Manager published returns only published posts
#     context = {'title': 'main page',
#                'menu': menu,
#                'posts': posts,
#                'cat_selected': 0
#                }
#     return render(request, 'index.html', context) #render handles template and returns it to the client


class MenHome(ListView): # CBV version of function based index view
    model = Men #queryset/ displays all the posts: both published and not, to display only published we need method get_queryset
    template_name = 'index.html'
    context_object_name = 'posts' # redetermine default name, which is 'object_list'
    extra_context = { #to display menu fields (in our case) and some other things # can only convey static data that already exist, for dynamic data we use def get_context_data(self):
        'title': 'main page',
        'menu': menu,
        'cat_selected': 0,

    }

    def get_queryset(self):
        return Men.published.all().select_related('cat')#displays only published posts, select_related('cat') displays posts belonging to a selected category



    def get_context_data(self, **kwargs): #for dynamic data
        context = super().get_context_data(**kwargs)
        context['cat_selected'] = int(self.request.GET.get('cat_id', 0)) #adds dynamicly changed category, from the address line
        return context



# def show_post(request, post_slug): func based view is replaced by class based view ShowPost
#     post = get_object_or_404(Men, slug=post_slug)
#
#     context = {
#         'title': post.title,
#         'menu': menu,
#         'post': post,
#         'cat_selected': 1
#
#     }
#     return render(request, 'post.html', context)


class ShowPost(DetailView):
    model = Men
    template_name = 'post.html'
    slug_url_kwarg = 'post_slug' # we have to define this field, or else error, because slug: post_slug is a custom name, if it was pk or slug then would be ok
    # pk_url_kwarg = #define if we search by pk, but we use slug so we dont need this field
    context_object_name = 'post' # in detail view by default uses name 'object'

    def get_context_data(self, **kwargs):# to add title to our page, we need to customize this method
        context = super().get_context_data(**kwargs)
        context['title'] = context['post'].title
        context['menu'] = menu
        return context

    def get_object(self, queryset=None):# in order not to display not published pages (it's like get_queryset but for detail view)
        return get_object_or_404(Men.published, slug=self.kwargs[self.slug_url_kwarg]) #we passed manager published to display only published posts by their slug

# def handle_uploaded_file(f): # function from django documentation, f is an object that we are uploading
#     with open(f'uploads/{f.name}', "wb+") as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)


def about(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)# because we upload files we need to write FILES here
        # handle_uploaded_file(request.FILES['file_upload']) #key file_upload appeared because we defined the class='file_upload' in our html template about.html /name is our key:     <p><input type="file" name="file_upload"></p>
        if form.is_valid(): # checks wheter the fields are correct
            # handle_uploaded_file(form.cleaned_data['file']) # file is the name of the field in the UploadFileForm//now we comment it because we upload via models and use different class for it
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()#these two lines fp replaced the function: handle_uploaded_file # formbased upload replaced by modelbased upload
    else:
        form = UploadFileForm()
    return render(request, 'about.html', {'title':'about', 'menu': menu, 'form': form}) #also added form attribute

# def addpage(request): #also replaced by AddPage
#     if request.method == 'POST':# once the user clicked the button 'enter or post' then form is being filled by entered data/also browser checks the correctness of the data
#         form = AddPostForm(request.POST, request.FILES)#to save not only text but photos or files we need to add request.FILES
#         if form.is_valid():# the server validates the data(step 2)
#             # print(form.cleaned_data) # displays dictionary type trusted data
#             # try: # after we wrote class Meta in form AddPostForm we have got a new method 'save'... so now we change block try: except:
#             #     Men.objects.create(**form.cleaned_data)# ** unpacks dictionary cleaned_data#trying to save the cleaned data to the db
#             #     return redirect('index')#after success get redirected to the home page
#             # except:
#             #     form.add_error(None, 'creation post error')#if not succeeded then display errors
#             form.save()
#             return redirect('index')
#     else:
#         form = AddPostForm()# when form displays first time, then method GET and empty form
#     context = {
#         'menu': menu,
#         'title': 'add page',
#         'form': form
#     }
#     return render(request, 'addpage.html', context)
#


#addpage but class based view
class AddPage(View):
    def get(self, request):
        form = AddPostForm()
        context = {
            'menu': menu,
            'title': 'Add article',
            'form': form
        }
        return render(request, 'addpage.html', context)

    def post(self, request):
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
        context = {
            'menu': menu,
            'title': 'Add article',
            'form': form
        }
        return render(request, 'addpage.html', context)



def contact(request):
    return HttpResponse('contact')

def login(request):
    return HttpResponse('login')

# def show_category(request, cat_slug): func based view is replaced by class based view MenCategory
#     category = get_object_or_404(Category, slug=cat_slug) # (first argument (Category)- choose model from which we need to get something, second argument (slug) is a criterion based on which we need to select posts/ slug = cat_slug
#     posts = Men.published.filter(cat_id=category.pk).select_related('cat') # returns posts whose id equals slug we read above
# # we use select_related('cat') in order to eliminate repetitive SQL requests, it optimises the website ()
#     context = {'title': f'Category: {category.name}',
#                'menu': menu,
#                'posts': posts,
#                'cat_selected': category.pk
#                }
#     return render(request, 'index.html', context)


class MenCategory(ListView): # class based view of show_category
    template_name = 'index.html'
    context_object_name = 'posts'
    allow_empty = False # list  posts' in cat in get_context_data. is empty then 404/ if wrong slug then 404

    def get_queryset(self):
        return Men.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')#cat_slug came from urls <slug:cat_slug>


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat # takes first piece of data from the dict
        context['title'] = 'Category - ' + cat.name
        context['menu'] = menu
        context['cat_selected'] = cat.pk
        return context




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

# def show_tag_postlist(request, tag_slug): func based view is replaced by class based view TagPostList
#     tag = get_object_or_404(TagPost, slug=tag_slug)
#     posts = tag.tags.filter(is_published=Men.Status.PUBLISHED).select_related('cat')
#     context = {
#         'title': f'Tag: {tag.tag}',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': None
#     }
#     return render(request, 'index.html', context)

class TagPostList(ListView):
    template_name = 'index.html'
    context_object_name = 'posts'
    allow_empty = False
    def get_queryset(self):
        return Men.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        context['title'] = 'Tag: - ' + tag.tag
        context['menu'] = menu
        context['cat_selected'] = None
        return context