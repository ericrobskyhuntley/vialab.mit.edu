from django.urls import path

from . import views

app_name = 'classes'
urlpatterns = [
    path('', views.ClassesListView.as_view(), name='classes'),
    path('instance/<slug:slug>/', views.class_instance_detail, name='class_instance'),
]