from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse, reverse_lazy
from django.template.defaultfilters import slugify
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView, DeleteView

from .forms import AddPostForm, UploadFileForm
from .models import Men, Category, TagPost, UploadFiles
from django.views import View

from .utils import DataMixin

# Create your views here.


# menu = [{'title': 'about us', 'url_name': 'about'},
#         {'title': 'add article', 'url_name': 'add_page'},
#         {'title': 'feedback', 'url_name': 'contact'},
#         {'title': 'login', 'url_name': 'login'}
# ] #because of defining it in mixin(utils.py) we don't need it here anymore




# def index(request): # replaced by MenHome
#     posts = Men.published.all().select_related('cat') # Manager published returns only published posts
#     context = {'title': 'main page',
#                'menu': menu,
#                'posts': posts,
#                'cat_selected': 0
#                }
#     return render(request, 'index.html', context) #render handles template and returns it to the client


class MenHome(DataMixin, ListView): # CBV version of function based index view
    model = Men #queryset/ displays all the posts: both published and not, to display only published we need method get_queryset
    template_name = 'index.html'
    context_object_name = 'posts' # redetermine default name, which is 'object_list'
    title_page = 'main page'#title_page is our own field, we have to define it in mixins
    cat_selected = 0
    # extra_context = { #to display menu fields (in our case) and some other things # can only convey static data that already exist, for dynamic data we use def get_context_data(self):
    #     'title': 'main page',
    #     'menu': menu,
    #     'cat_selected': 0,
    #
    # }#remove extra_context because of using mixins

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


class ShowPost(DataMixin, DetailView): #added mixin DataMixin
    model = Men
    template_name = 'post.html'
    slug_url_kwarg = 'post_slug' # we have to define this field, or else error, because slug: post_slug is a custom name, if it was pk or slug then would be ok
    # pk_url_kwarg = #define if we search by pk, but we use slug so we dont need this field
    context_object_name = 'post' # in detail view by default uses name 'object'

    def get_context_data(self, **kwargs):# to add title to our page, we need to customize this method
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)#using mixins
        # context['title'] = context['post'].title #we put this line above because of using mixins
        #context['menu'] = menu #dont need this anymore, mixins
        #return context

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
    return render(request, 'about.html', {'title':'about', 'form': form}) #also added form attribute

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

class AddPage(DataMixin, CreateView): #replace FormView on CreateView and remove method form_valid, because it already exists in CreateView
    form_class = AddPostForm #link on the form class
    #instead of form_class we can write model=Men and fields = ['write fields we want to be displayed, make sure to include all compulsory fields']
    template_name = 'addpage.html'
    #in CreateView we can remove success_url then it will use get_absolute_url from models, but we should determine it in advance
    success_url = reverse_lazy('index')# the same as reverse, builds the url only when its necessary, not immediately like function reverse does. it helps to avoid errors
    #to add menu fields we need extra_context
    title_page = 'add article' #this line defined in mixins, put it here instead of extra_context
    # extra_context = {
    #     'menu': menu,
    #     'title': 'add article'
    # }#using mixin, this extra_context also don't need
    # it does not save the data to the db yet
    # to do so we need to call form_valid method, it gets called only after all the fields in the form are checked and correct(validated)

    # def form_valid(self, form):#remove this method after replacing FormView on CreateView, it already exists in CreateView
    #     form.save()
    #     return super().form_valid(form)


class UpdatePage(DataMixin, UpdateView):
    #we used 'model' and 'fields' because we didn't define form_class before
    model = Men
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'addpage.html'
    success_url = reverse_lazy('index')
    title_page = 'edit article'
    # extra_context = {
    #     'menu': menu,
    #     'title': 'Alter the article'
    # }the same as in AddPage

class DeletePage(DeleteView):
    model = Men
    success_url = reverse_lazy('index')
    template_name = 'men_confirm_delete.html'#after deleting an article it requires confirmation, which is located on this address


# class AddPage(View):#addpage but class based view # later it is replaced by FormView
#     def get(self, request):
#         form = AddPostForm()
#         context = {
#             'menu': menu,
#             'title': 'Add article',
#             'form': form
#         }
#         return render(request, 'addpage.html', context)
#
#     def post(self, request):
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('index')
#         context = {
#             'menu': menu,
#             'title': 'Add article',
#             'form': form
#         }
#         return render(request, 'addpage.html', context)



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


class MenCategory(DataMixin, ListView): # class based view of show_category
    template_name = 'index.html'
    context_object_name = 'posts'
    allow_empty = False # list  posts' in cat in get_context_data. is empty then 404/ if wrong slug then 404

    def get_queryset(self):
        return Men.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')#cat_slug came from urls <slug:cat_slug>


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat # takes first piece of data from the dict
        return self.get_mixin_context(context, title='category- ' + cat.name, cat_selected=cat.pk,)#added with mixins

        #the lines below don't need after adding the line above with mixins
        # context['title'] = 'Category - ' + cat.name
        # context['menu'] = menu
        # context['cat_selected'] = cat.pk
        # return context




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

class TagPostList(DataMixin, ListView):
    template_name = 'index.html'
    context_object_name = 'posts'
    allow_empty = False
    def get_queryset(self):
        return Men.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Tag: ' + tag.tag)#added with mixin

        #no need because of adding the line above and mixins
        # context['title'] = 'Tag: - ' + tag.tag
        # context['menu'] = menu
        # context['cat_selected'] = None
        # return context