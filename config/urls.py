"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path as url

urlpatterns = [
    #url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),

    path('admin/', admin.site.urls),
    #url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

    path('', include('personal.urls')),
    path('account/', include('account.urls')),
    path('my-account/', include('myaccount.urls')),
    path('notification/', include('notification.urls')),
    path('book/', include('book.urls')),
    path('likeordislike/', include('likeordislike.urls')),
    path('aboutbook/', include('aboutbook.urls')),
    path('comment/', include('comment.urls')),
    path('question/', include('question.urls')),
    path('chat/', include('chat.urls')),
    
    
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    #urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)