from django.contrib import admin
from .models import Class, ClassInstance, SessionTime, SessionType, InstructorOrder

class SessionInline(admin.TabularInline):
    model = SessionType
    extra = 1

class InstructorsInline(admin.TabularInline):
    model = InstructorOrder
    extra = 1

class ClassInstanceAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)
    inlines = (SessionInline,InstructorsInline,)

# Register your models here.
admin.site.register(Class)
admin.site.register(ClassInstance, ClassInstanceAdmin)
admin.site.register(SessionTime)