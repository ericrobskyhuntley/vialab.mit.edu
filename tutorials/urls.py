from django.urls import path, re_path

from . import views

app_name = 'tutorials'
urlpatterns = [
    path('', views.module_list, name='modules'),
    path('series/', views.serieses, name='serieses'),
    path('module/<slug:slug>/', views.module, name='module'),
    path('serieses/<int:series_id>/', views.series, name='series')
]