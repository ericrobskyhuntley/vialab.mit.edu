"""vialab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from .views import markdown_uploader

urlpatterns = [
    path('classes/', include('classes.urls')),
    path('calendar/', include('cal.urls')),
    path('reading/', include('reading.urls')),
    path('people/', include('people.urls')),
    path('tutorials/', include('tutorials.urls')),
    path('', include('main.urls')),
    path('admin/', admin.site.urls),
    # Necessary for Martor.
    path('martor/', include('martor.urls')),
    path('api/uploader/', markdown_uploader, name="markdown_uploader_page"),
    path('markdownx/', include('markdownx.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
