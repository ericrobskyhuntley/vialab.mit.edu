from django.shortcuts import get_object_or_404, render
from datetime import date
from django.views import generic
from el_pagination.views import AjaxListView
from datetime import date, timedelta, datetime
from .models import Event

def event_list(request,
    template='cal/event_list.html',
    page_template='cal/event_list_page.html'):
    context = {
        'current_upcoming': Event.objects.filter(
            day__gte=date.today()
        ).prefetch_related(
            'participant'
        ).prefetch_related(
            'topics'
        ).select_related(
            'venue'
        ).select_related(
            'module'
        ).order_by('day'),
        'page_template': page_template,
    }
    if request.is_ajax():
        template = page_template
    return render(request, template, context)

# class EventListView(AjaxListView):
#     """
#     Event list view, which splits events into current/upcoming
#     and past. The latter is paginated using el-pagination.
#     """
#     context_object_name = 'event_list'
#     template_name = 'cal/event_list.html'
#     page_template = 'cal/event_list_list_page.html'

#     def get_queryset(self):
#         """
#         Get archived events (prior to current day).
#         """
#         return Event.objects.filter(
#             day__lt=date.today()
#         ).prefetch_related(
#             'participant'
#         ).prefetch_related(
#             'topics'
#         ).select_related(
#             'venue'
#         ).select_related(
#             'module'
#         ).order_by('day')

#     def get_context_data(self, **kwargs):
#         context = super(EventListView, self).get_context_data(**kwargs)
#         """
#         Get current and upcoming events.
#         """
#         context['current_upcoming'] = Event.objects.filter(
#             day__gte=date.today()
#         ).prefetch_related(
#             'participant'
#         ).prefetch_related(
#             'topics'
#         ).select_related(
#             'venue'
#         ).select_related(
#             'module'
#         ).order_by('day')
#         return context

class EventDetailView(generic.DetailView):
    model = Event
    template_name = 'cal/event_detail.html'
    context_object_name = 'event_detail'