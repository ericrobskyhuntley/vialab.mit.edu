from django.urls import path

from . import views

app_name = 'reading'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:reading_id>/', views.reading_list, name='reading_list'),
]