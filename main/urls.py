from django.urls import path

from . import views

app_name = 'main'
urlpatterns = [
    path('colophon/', views.colophon, name='colophon'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('', views.landing, name='landing')
]