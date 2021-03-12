from django.db import models
from django.conf import settings
from django.utils.functional import cached_property
from martor.models import MartorField

from people.models import Person
from simple_history.models import HistoricalRecords

from .zotero import fetch_list

class ReadingMetadata(models.Model):
    name = models.CharField(max_length=25)
    desc = MartorField(max_length=2000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords(
        history_change_reason_field=models.TextField(null=True)
    )

    class Meta:
        verbose_name = "reading list app metadata"
        verbose_name_plural = "reading list app metadata"

    def __str__(self):
        return self.name

# Create your models here.
class ReadingList(models.Model):
    title = models.CharField(max_length=200)
    author = models.ManyToManyField(Person)
    desc = MartorField(max_length=1000, blank=True)
    LIB_TYPES = [
        ('user', 'User Library'),
        ('group', 'Group Library'),
    ]
    lib_type = models.CharField(
        max_length=5,
        choices=LIB_TYPES,
        default='group',
    )
    CITE_STYLES = [
        ('mla', 'Modern Language Association (MLA)'),
        ('chicago-author-date', 'Chicago (Author Date)'),
        ('taylor-and-francis-harvard-x', 'Harvard'),
    ]
    cite_style = models.CharField(
        max_length=30,
        choices=CITE_STYLES,
        default='chicago-author-date',
    )
    library_id = models.IntegerField()
    collection_key = models.CharField(max_length=20, default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords(
        history_change_reason_field=models.TextField(null=True)
    )
    @cached_property
    def list_html(self):
        return fetch_list(
            library_id = self.library_id, 
            library_type = self.lib_type, 
            collection_key = self.collection_key,
            api_key = settings.ZOTERO_KEY, 
            csl = self.cite_style
            )

    class Meta:
        verbose_name = "reading list"
        verbose_name_plural = "reading lists"
    def __str__(self):
        return self.title