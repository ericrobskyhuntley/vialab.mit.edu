from .models import MainMetadata
from tutorials.models import TutorialsMetadata
from reading.models import ReadingMetadata
from cal.models import EventMetadata
from people.models import PeopleMetadata
from cal.models import Event
from datetime import date

def get_site_data(request):
    try:
        site_data = MainMetadata.objects.latest('created_at')
    except MainMetadata.DoesNotExist:
        site_data = None
    try:
        tutorials_meta = TutorialsMetadata.objects.latest('created_at')
    except TutorialsMetadata.DoesNotExist:
        tutorials_meta = None
    try:
        reading_meta = ReadingMetadata.objects.latest('created_at')
    except ReadingMetadata.DoesNotExist:
        reading_meta = None
    try:
        cal_meta = EventMetadata.objects.latest('created_at')
    except EventMetadata.DoesNotExist:
        cal_meta = None
    try:
        people_meta = PeopleMetadata.objects.latest('created_at')
    except PeopleMetadata.DoesNotExist:
        people_meta = None
    try:
        upcoming_events = Event.objects.filter(day__gte=date.today()).order_by('-day')[:3]
    except:
        upcoming_events = None
    return {
        'site_data': site_data,
        'tutorials_meta': tutorials_meta,
        'reading_meta': reading_meta,
        'cal_meta': cal_meta,
        'upcoming_events': upcoming_events,
        }