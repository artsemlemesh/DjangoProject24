from men.utils import menu


def get_men_context(request):#any name
    return {'mainmenu': menu} # this dictionary automatically passed to all the templates
#then we should connect it in settings: add this line: 'users.context_processors.get_men_context' to settings/ TEMPLATES / context_processors