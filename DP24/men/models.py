from django.db import models
from django.urls import reverse


# Create your models here.


class PublishManager(models.Manager):
     def get_queryset(self):
         return super().get_queryset().filter(is_published=Men.Status.PUBLISHED)

class Men(models.Model):
    class Status(models.IntegerChoices): #class Status(can be any name) for field is_published, 1 publ, 0 not,
        DRAFT = 0, 'draft'
        PUBLISHED = 1, 'published'

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)#db_index displays articles faster
    content = models.TextField(blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT)
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
        ordering = ['-time_created'] #returns posts after sorting it by time
        indexes = [models.Index(fields=['-time_created'])]

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug}) # key post_slug we take from urls where <slug:post_slug>


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
# c = Category.objects.get(pk=2) - get category #2
# c.men_set.all() - returns all the posts related to the category
# if in the field cat we add related_name='posts', then c.men_set.all() == c.posts.all()
# we use __ for lookups like Category.objects.filter(pk__gte=1) and also to refer to a field of another model: Men.objects.filter(cat__slug='singers')
    def __str__(self):
        return self.name

#Category.objects.filter(posts__title__contains='o') -inner join(joins 2 tables) returns name of categories of posts where title contains letter o) <QuerySet [<Category: singers>, <Category: singers>, <Category: acters>, <Category: acters>]>
#Catogory.objects.filter(posts__title__contains='o').distinct() returns only unique names of groups <QuerySet [<Category: singers>, <Category: acters>]>

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug}) # key cat_slug we take from url where <slug:cat_slug> and then in out template we can just insert in link {{ cat.get_absolute_url }}

class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

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
#w = Wife.objects.all().annotate(is_married=Value(True))
#w1 = Wife.objects.all().annotate(work_age=F('age')-10)

