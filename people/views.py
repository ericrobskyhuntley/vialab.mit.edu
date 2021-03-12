from django.shortcuts import get_object_or_404, render
from django.http import Http404
from .models import Person

# Create your views here.
def index(request):
    people = Person.objects.all()
    return render(request, 'people/index.html', {
        'people': people}
    )

# def person(request, person_id):
#     person = get_object_or_404(Person, pk=person_id)
#     return render(request, 'people/person_detail.html', {'person': person})

def person_detail(request, slug):
    selection = Person.objects.all()
    person = get_object_or_404(selection, slug = slug)
    return render(request, 'people/person_detail.html', {
        'person': person
        }
    )