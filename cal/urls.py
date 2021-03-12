from django.urls import path
from . import views

app_name = 'cal'
urlpatterns = [
    path('', views.event_list, name='calendar'),
    path('event/<slug:slug>/', views.EventDetailView.as_view(), name='event_detail'),
]