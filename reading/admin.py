from django.contrib import admin
from .models import ReadingList, ReadingMetadata
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.
admin.site.register(ReadingList, SimpleHistoryAdmin)
admin.site.register(ReadingMetadata, SimpleHistoryAdmin)