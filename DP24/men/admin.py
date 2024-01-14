from django.contrib import admin, messages

from .models import Men, TagPost, Wife, Category


admin.site.register(TagPost)
admin.site.register(Wife)


class MarriedFilter(admin.SimpleListFilter): #before the main class we should write class that determines our filter
    title = 'status of men'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('married', 'Married'),
            ('single', 'Not married')
        ]
    def queryset(self, request, queryset):
        if self.value() == 'married':
            return queryset.filter(wife__isnull=False)# we are in Men class, using __ because isnull is a lookup filter
        elif self.value() == 'single':
            return queryset.filter(wife__isnull=True)



@admin.register(Men)
class MenAdmin(admin.ModelAdmin):
    list_display = ('title', 'time_created', 'is_published', 'cat', 'brief_info')
    list_display_links = ('title',) # fields that have links, by defauld only id field is clickable
    ordering = ['time_created', 'title'] # can wrap in both tuple or list/ sorts posts by time_created, for those whose time is the same sorts by next field ( title )
    list_editable = ('is_published',) #should put comma at the end to make it to be tuple (list_editable) returns a tuple of fields that can be edited in django admin panel
    list_per_page = 10 #pagination in admin panel (3 posts per page)
#admin.site.register(Men, MenAdmin) the same like this line: @admin.register(Men)
#if we want to put a field in (list_editable) we have to remove the field from (list_display_links)
#if don't use comma in tuple then error. correct ('title', )
    actions = ['set_published', 'unpublish'] #to display method set_published in action menu of django-admin
    search_fields = ['title', 'cat__name'] #adds search panel and looks in titles field, add cat__name not cat(not a field, but a key), __ can add lookups or fields / searches in two fields
    list_filter = [MarriedFilter, 'cat__name', 'is_published'] #adds filtration table to the right side
    # to include our custom filter class we just need to add it to list filter exactly like shown above(without brackets, just send the link to it)
    @admin.display(description='brief_info', ordering='content') #ordering=sort, can use only fields from db, brief_info does not exist in db, so we can link ordering to some other fields
    def brief_info(self, men: Men):
        return f'Description {len(men.content)} symbols'

    @admin.action(description='publish selected posts') #changes the name from 'set_publish' to choosen one
    def set_published(self, request, queryset):#this method adds extra option to action field in django admin #request is an object or request, queryset -object of choosen posts/
        count = queryset.update(is_published=Men.Status.PUBLISHED) #sets posts to published
        self.message_user(request, f'{count} posts were published') # notifies use in django admin on how many posts were changed

    @admin.action(description='unpublish selected posts')
    def unpublish(self, request, queryset):
        count = queryset.update(is_published=Men.Status.DRAFT)
        self.message_user(request, f'{count} posts were unpublished', messages.WARNING)# flag warning # when unpublished and messages.WARNING displays exclamation mark in yellow triangle instead of green tick

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
#admin.site.register(Category, CategoryAdmin)
