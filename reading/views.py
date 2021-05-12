from django.shortcuts import get_object_or_404, render
from .models import ReadingList

# Create your views here.
def reading_lists(request):
    reading_lists = ReadingList.objects.all()
    return render(request, 'reading/reading_list_list.html', {
        'reading_lists': reading_lists
        }
    )

def reading_list_detail(request, slug):
    reading_list = get_object_or_404(ReadingList, slug = slug)
    return render(request, 'reading/reading_list_detail.html', {
        'reading_list': reading_list
        }
    )