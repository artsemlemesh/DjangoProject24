from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


# Create your models here.


class PublishManager(models.Manager):
     def get_queryset(self):
         return super().get_queryset().filter(is_published=Men.Status.PUBLISHED)

class Men(models.Model):
    class Status(models.IntegerChoices): #class Status(can be any name) for field is_published, 1 publ, 0 not,
        DRAFT = 0, 'draft'
        PUBLISHED = 1, 'published'

    title = models.CharField(max_length=255, verbose_name='My_title') # verbose_name changes the name of the columns in django admin panel
    slug = models.SlugField(max_length=255, unique=True, db_index=True)#db_index displays articles faster
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', default=None,
                              blank=True, null=True, verbose_name='Photo')#we define photo field later than others, and in order to successfully apply migrations we need null=True
    content = models.TextField(blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), (Status.choices))), #crutch for admin panel which helps properly display 'draft' and 'published' posts and alter them there/(helps to work a widget) we need to do it to convert integerChoices into booleanfield
                                       default=Status.DRAFT)
    cat = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='posts') #CASCADE is not parameter() it is function, and here we pass a link on the function
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags')#tags-manager #related_name - to get a list of articles through tags that are connected with them
    wife = models.OneToOneField('Wife', on_delete=models.SET_NULL, null=True, blank=True, related_name='husband')
    # here name is cat, but in db it is cat_id, because of ForeignKey, _id has automatically been added
    # m = Men.objects.get(pk=1)
    # m.cat (sql request) will return <Category: acters>/ m.cat.name or m.cat.slug will return name and slug of a category model respectively
    # m.cat_id (no sql, just number returns) will return 1 - id of the category that this post belongs to

    objects = models.Manager()
    published = PublishManager()
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Famous men' # changes the name of the class in django admin panel
        verbose_name_plural = 'Famous men' # to remove letter s at the end of the word in django admin panel
        ordering = ['-time_created'] #returns posts after sorting it by time
        indexes = [models.Index(fields=['-time_created'])]

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug}) # key post_slug we take from urls where <slug:post_slug>

    # def save(self, *args, **kwargs): # save is an object of class Men, when it gets called it applies to the current post
    #     self.slug = slugify(self.title) # we can determine attribute slug for a current post here
    #     super().save(*args, **kwargs)
        #slugify lets create the slug based on the title
    #!!!!this is one of the options to create slug field automatically, I use better one, In file admin.py for the model i added field: prepopulated_fields = {'slug': ('title', )}

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='name_of_category')
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
# c = Category.objects.get(pk=2) - get category #2
# c.men_set.all() - returns all the posts related to the category
# if in the field cat we add related_name='posts', then c.men_set.all() == c.posts.all()
# we use __ for lookups like Category.objects.filter(pk__gte=1) and also to refer to a field of another model: Men.objects.filter(cat__slug='singers')
# Category.objects.annotate(total=Count('posts')) #returns Category table with extra temperary column "total", reverse linking accesses related_name='posts' from Men class
# c = Category.objects.annotate(total=Count('posts')).filter(total__gt=1) # returns categories that have more than one post
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

#Category.objects.filter(posts__title__contains='o') -inner join(joins 2 tables) returns name of categories of posts where title contains letter o) <QuerySet [<Category: singers>, <Category: singers>, <Category: acters>, <Category: acters>]>
#Catogory.objects.filter(posts__title__contains='o').distinct() returns only unique names of groups <QuerySet [<Category: singers>, <Category: acters>]>

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug}) # key cat_slug we take from url where <slug:cat_slug> and then in out template we can just insert in link {{ cat.get_absolute_url }}

class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

# tag = TagPost.objects.annotate(total=Count('tags')).filter(total__gt=1) # returns number of tags that contain more than one post /(tags)-reverse linkin with class Men
    def __str__(self):
        return self.tag

    def get_absolute_url(self): #something is wrong with this function. it doesnot work in my list_tags.html template
        return reverse('tag', kwargs={'tag_slug', self.slug})  #slug retrieves from the database and via the variable 'tag_slug' gets inserted to the itinerary (link)



class Wife(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    m_count = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.name


#w1 = Wife.objects.create(name='Margaret', age=39)
#w1.husband (related_name of a field wife in Men model) will return husband of w1

#m1 = Men.objects.get(pk=1)
# m1.wife(field in Men class) = w1
#m1.save() - will attach w1 to m1/ important!! m1.save() //save changes in the table where the changes occured. in my case in table m1 was added w1



#Querysets: first() last()
#m = Men.objects.get(pk=1)
#m.get_previous_by_time_updated (write this: get_previous_by and add name of any time field after) - will return previous...
#m.get_next_by_time_updated()...

#exists() - to check whether this post exists in the db/ count() number of posts
#c3 = Category.objects.create(name='scientists', slug='scientist')
#c3.posts.exists() -if nothing returns False, if something returns True

# to call custom shell: python3 manage.py shell_plus --print-sql

#F string and annotate
#w = Wife.objects.all().annotate(is_married=Value(True)) #creates a temporary field (is_married) without changing db
#w1 = Wife.objects.all().annotate(work_age=F('age')-10)

#Aggregate (Sum, Avg, Max, Min, values())
#w = Wife.objects.aggregate(res=Max('age')-Min('age')) # returns age difference btw max and min

#m = Men.objects.values('title', 'cat__name', 'wife__name').get(pk=1) # returns only values of these three columns, __ refers to another class (inner join)


#upload files via models, previousely we did via forms into directory uploads

class UploadFiles(models.Model): #upload via models rather than forms allowed us to upload the same file many times(instead of just rewriting it) it adds unique name in case of uploading the same file name
    file = models.FileField(upload_to='uploads_model')