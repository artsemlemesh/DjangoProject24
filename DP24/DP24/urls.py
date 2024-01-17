"""
URL configuration for DP24 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from DP24 import settings
from men.views import page_not_found

urlpatterns = [
    path("admin/", admin.site.urls),
    path('men/', include('men.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]

if settings.DEBUG: # setting the address to display uploaded picture on the page
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = page_not_found  #when DEBUG=False and address not found, user-friendly page will be displayed

admin.site.site_header = 'Mike\'s webpanel' # changes the name of the django admin panel
admin.site.index_title = 'Test website'