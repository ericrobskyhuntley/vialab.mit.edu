from django.shortcuts import get_object_or_404, render
from django.http import Http404
from .models import MainMetadata
from cal.models import Event
from classes.models import ClassInstance
from cal.models import Event

from datetime import date, timedelta


# Create your views here.
def about(request):
    about = MainMetadata.objects.latest('created_at')
    return render(request, 'main/about.html', {
        'about': about,
        }
    )
def colophon(request):
    meta = MainMetadata.objects.latest('created_at')
    return render(request, 'main/colophon.html', {
        'meta': meta,
        }
    )
def contact(request):
    contact = MainMetadata.objects.latest('created_at')
    return render(request, 'main/colophon.html', {
        'contact': contact,
        }
    )

def landing(request):
    today = date.today()
    end_date = today + timedelta(weeks=20)
    current_upcoming = ClassInstance.objects.select_related(
            'cl__institution'
        ).select_related(
            'semester'
        ).filter(
            semester__end__range=[today, end_date]
        ).prefetch_related(
            'sessions'
        ).order_by('semester__start')

    upcoming_events = Event.objects.filter(
            day__gte=today
        ).order_by('day')[0:5]
    
    return render(request, 'main/landing.html', {
        'current_upcoming': current_upcoming,
        'upcoming_events': upcoming_events
        }
    )