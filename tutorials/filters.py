import django_filters
from django import forms
from django.db.models import Count

from .models import Software, Skill, Module, Series

class SeriesFilter(django_filters.FilterSet):
    software = django_filters.ModelChoiceFilter(
        field_name = 'module__software__name',
        queryset=Software.objects.all(),
        label = 'Software',
        widget=forms.Select(attrs={'onchange': 'this.form.submit();'})
        )
    skills = django_filters.ModelChoiceFilter(
        field_name = 'module__skills__name',
        queryset=Skill.objects.all(),
        label = 'Skills',
        widget=forms.Select(attrs={'onchange': 'this.form.submit();'})
        )
    class Meta:
        model = Series
        distinct = True
        fields = ['software', 'skills']

class ModuleFilter(django_filters.FilterSet):
    software = django_filters.ModelChoiceFilter(
        queryset=Software.objects.annotate(c=Count('module')).filter(c__gt=0),
        empty_label="Any Software"
    )
    skills = django_filters.ModelChoiceFilter(
        queryset=Skill.objects.annotate(c=Count('module')).filter(c__gt=0),
        empty_label="Any Skills"
    )