from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import MainMetadata

# Register your models here.
admin.site.register(MainMetadata, SimpleHistoryAdmin)