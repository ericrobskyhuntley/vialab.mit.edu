from django.shortcuts import get_object_or_404, render
from classes.models import ClassInstance

from el_pagination.views import AjaxListView
from datetime import date, timedelta

class ClassesListView(AjaxListView):
    context_object_name = 'class_list'
    template_name = 'classes/class_instance_list.html'
    page_template = 'classes/class_instance_list_page.html'

    def get_queryset(self):
        """Return the last ten published posts."""
        today = date.today()
        classes = ClassInstance.objects.select_related(
            'cl__institution'
        ).select_related(
            'semester'
        ).filter(
                semester__end__lt=today
        ).prefetch_related(
            'sessions'
        ).order_by('-semester__start')
        return classes

    def get_context_data(self, **kwargs):
        today = date.today()
        context = super(ClassesListView, self).get_context_data(**kwargs)
        context['current_upcoming'] = ClassInstance.objects.select_related(
            'cl__institution'
        ).select_related(
            'semester'
        ).filter(
                semester__end__gte=today
        ).prefetch_related(
            'sessions'
        ).order_by('semester__start')
        return context

# Create your views here.
def class_instance_detail(request, slug):
    selection = ClassInstance.objects.select_related(
            'cl__institution'
        ).select_related(
            'semester'
        ).prefetch_related(
            'sessions'
        ).prefetch_related(
            'instructors'
        ).prefetch_related(
            'software'
        ).prefetch_related(
            'skills'
        ).order_by(
            'instructors__instructor_order'
        )
    class_instance = get_object_or_404(selection, slug = slug)
    return render(request, 'classes/class_instance_detail.html', {
        'class_instance': class_instance
        }
    )