from django.shortcuts import get_object_or_404, render
from django.http import Http404
from tutorials.models import Module, Series
from tutorials.filters import ModuleFilter
from tutorials.models import Software, Episode
from people.models import Person
from el_pagination.views import AjaxListView

# Create your views here.
def index(request):
    featured_series = Series.objects.filter(featured = True).order_by('-created_at')[0]
    latest_series = SeriesFilter(
        request = request.GET,
        queryset = Series.objects.filter(featured = False).order_by('-created_at')
        )
    featured_module = Module.objects.filter(featured = True).order_by('-created_at')[0]
    latest_modules = ModuleFilter(
        request = request.GET,
        queryset = Module.objects.filter(featured = False).order_by('-created_at')
        )
    return render(request, 'tutorials/index.html', {
        'featured_series': featured_series,
        'latest_series': latest_series,
        'featured_module': featured_module,
        'latest_modules': latest_modules,
        }
    )

def serieses(request):
    featured = Series.objects.filter(featured = True).order_by('-created_at')[0]
    queryset = SeriesFilter(
        request = request.GET,
        queryset = Series.objects.all(),
        )
    return render(request, 'tutorials/serieses.html', {
        'featured': featured,
        'serieses': queryset,
        }
    )

def module_list(request,
    template='tutorials/module_list.html',
    page_template='tutorials/module_list_page.html'):
    context = {
        'modules': ModuleFilter(request.GET,
            queryset = Module.objects.all()
        ),
        'page_template': page_template,
    }
    if request.is_ajax():
        template = page_template
    return render(request, template, context)

def series(request, series_id):
    series = get_object_or_404(Series, pk = series_id)
    return render(request, 'tutorials/series.html', {
        'series': series,
        }
    )

def module(request, slug):
    module = get_object_or_404(Module, slug = slug)
    return render(request, 'tutorials/module_detail.html', {
        'module': module
        }
    )