from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Person, Institution, Affiliation, PeopleMetadata

class AffiliationInline(admin.TabularInline):
    model = Affiliation
    extra = 1

class PersonAdmin(admin.ModelAdmin):
    inlines = (AffiliationInline,)
    
class InstitutionAdmin(admin.ModelAdmin):
    inlines = (AffiliationInline,)

admin.site.register(Person, PersonAdmin)
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(Affiliation)
admin.site.register(PeopleMetadata)