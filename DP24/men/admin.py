from django.contrib import admin

from .models import Men, TagPost, Wife, Category


admin.site.register(TagPost)
admin.site.register(Wife)

@admin.register(Men)
class MenAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_created', 'is_published', 'cat')
    list_display_links = ('id', 'title') # fields that have links, by defauld only id field is clickable
    ordering = ['time_created', 'title'] # can wrap in both tuple or list/ sorts posts by time_created, for those whose time is the same sorts by next field ( title )
    list_editable = ('is_published',) #should put comma at the end to make it to be tuple (list_editable) returns a tuple of fields that can be edited in django admin panel
    list_per_page = 10 #pagination in admin panel (3 posts per page)
#admin.site.register(Men, MenAdmin) the same like this line: @admin.register(Men)
#if we want to put a field in (list_editable) we have to remove the field from (list_display_links)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
#admin.site.register(Category, CategoryAdmin)
