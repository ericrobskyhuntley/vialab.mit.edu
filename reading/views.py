from django.shortcuts import get_object_or_404, render
from .models import ReadingList

# Create your views here.
def index(request):
    reading_lists = ReadingList.objects.all()
    return render(request, 'reading/index.html', {
        'reading_lists': reading_lists
        }
    )

def reading_list(request, reading_id):
    reading_list = get_object_or_404(ReadingList, pk=reading_id)
    return render(request, 'reading/reading_list.html', {
        'reading_list': reading_list
        }
    )