from django.contrib import admin
from .models import Event, EventMetadata, Topic, Venue, Role, Semester, Days

# admin.site.register(Person, PersonAdmin)

class RoleInline(admin.TabularInline):
    model = Role
    extra = 1

class PersonInline(admin.ModelAdmin):
    inlines = (RoleInline,)

admin.site.register(Event, PersonInline)
admin.site.register(EventMetadata)
admin.site.register(Topic)
admin.site.register(Venue)
admin.site.register(Role)
admin.site.register(Semester)
admin.site.register(Days)