from django.urls import path

from . import views

app_name = 'reading'
urlpatterns = [
    path('', views.reading_lists, name='reading_lists'),
    path('<slug:slug>/', views.reading_list_detail, name='reading_list_detail'),
]