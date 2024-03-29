
menu = [{'title': 'about us', 'url_name': 'about'},
        {'title': 'add article', 'url_name': 'add_page'},
        {'title': 'feedback', 'url_name': 'contact'},
]



class DataMixin:
    paginate_by = 3
    title_page = None
    cat_selected = None#default
    extra_context = {}

    def __init__(self):# initializing title_page, because of using it first time in views
        if self.title_page:
            self.extra_context['title'] = self.title_page

        if self.cat_selected is not None:
            self.extra_context['cat_selected'] = self.cat_selected

        # if 'menu' not in self.extra_context: #remove this line because we use tag named get_menu
        #     self.extra_context['menu'] = menu
    def get_mixin_context(self, context, **kwargs):
        # context['menu'] = menu #remove this line because we use tag named get_menu
        context['cat_selected'] = None
        context.update(kwargs)
        return context
