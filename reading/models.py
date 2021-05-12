from django.db import models
from django.conf import settings
from django.utils.functional import cached_property
from martor.models import MartorField

from people.models import Person

import os

from .zotero import fetch_list
from django.template.defaultfilters import slugify

def banner_filename(instance, filename):
    path = 'images/banners/'
    fname, fext = os.path.splitext(filename)
    format = instance.slug + fext
    return os.path.join(path, format)

class ReadingMetadata(models.Model):
    name = models.CharField(max_length=25)
    desc = MartorField(max_length=2000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "reading list app metadata"
        verbose_name_plural = "reading list app metadata"

    def __str__(self):
        return self.name

# Create your models here.
class ReadingList(models.Model):
    banner = models.ImageField(null=True, blank=True, upload_to = banner_filename)
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
    collection_key = models.CharField(
        max_length=20, 
        default='',
        blank=True
    )
    slug = models.SlugField(
        default='',
        editable=False,
        unique=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    @property
    def zotero_url(self):
        if self.lib_type == 'group':
            base = '/'.join(['https://www.zotero.org/groups', str(self.library_id)])
            if self.collection_key and len(self.collection_key) > 0:
                return '/'.join([base, 'collections', self.collection_key])
            else:
                return base
    
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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = '-'.join((
                slugify(self.title),
                slugify(str(self.library_id)),
                slugify(str(self.collection_key))
            ))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title