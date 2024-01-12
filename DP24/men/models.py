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