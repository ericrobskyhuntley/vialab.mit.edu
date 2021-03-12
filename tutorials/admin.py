from django.db import models
from django.contrib import admin
from markdownx.models import MarkdownxField
from martor.widgets import AdminMartorWidget
from .models import Person, Series, Software, Skill, Module, Episode, TutorialsMetadata

class EpisodeInline(admin.TabularInline):
    model = Episode
    extra = 1

class SeriesAdmin(admin.ModelAdmin):
    inlines = (EpisodeInline,)
    
class ModuleAdmin(admin.ModelAdmin):
    inlines = (EpisodeInline,)
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }

admin.site.register(TutorialsMetadata)
admin.site.register(Series, SeriesAdmin)
admin.site.register(Software)
admin.site.register(Skill)
admin.site.register(Module, ModuleAdmin)