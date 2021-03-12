from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from martor.models import MartorField
from autoslug.settings import slugify as default_slugify
from autoslug import AutoSlugField

# Import other models.
from people.models import Person, Institution
from tutorials.models import Module

import os
import time

def banner_filename(instance, filename):
    path = 'images/banners/'
    fname, fext = os.path.splitext(filename)
    format = instance.title.replace(' ', '-').replace('.', '').replace(',','').lower() + '_' + str(round(time.time())) + fext
    return os.path.join(path, format)

class EventMetadata(models.Model):
    name = models.CharField(max_length=25)
    desc = MarkdownxField(max_length=1000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "event app metadata"
        verbose_name_plural = "event app metadata"

    def __str__(self):
        return self.name

class Topic(models.Model):
    name = models.CharField(max_length=250)
    definition = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "topic"
        verbose_name_plural = "topics"

    def __str__(self):
        return self.name

class Venue(models.Model):
    name = models.CharField(max_length=100)
    inst = models.ForeignKey(Institution, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "venue"
        verbose_name_plural = "venues"

    def __str__(self):
        return self.name

class Semester(models.Model):
    SEMESTERS = [
        ('S', 'Spring'),
        ('3', 'Spring (H3)'),
        ('4', 'Spring (H4)'),
        ('F', 'Fall'),
        ('1', 'Fall (H1)'),
        ('2', 'Fall (H2)'),
        ('I', 'IAP'),
        ('M', 'Summer'),
    ]
    semester = models.CharField(
        max_length=1,
        choices=SEMESTERS,
        default='T'
    )
    start = models.DateField(auto_now=False)
    end = models.DateField(auto_now=False)

    @property
    def year(self):
        return self.start.year

    def __str__(self):
        return self.get_semester_display() + ' ' + str(self.start.year)

class Event(models.Model):
    banner = models.ImageField(null=True, blank=True, upload_to = banner_filename)
    day = models.DateField()
    start = models.TimeField()
    end = models.TimeField()
    semester = models.ForeignKey(Semester, blank=True, null=True, on_delete=models.SET_NULL) 
    title = models.CharField(max_length=100)
    desc = MartorField()
    participant = models.ManyToManyField(Person, through='Role')
    topics = models.ManyToManyField(Topic)
    virtual_url = models.URLField(blank=True, null=True)
    cost = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        null=False,
    )
    ticket_url = models.URLField(blank=True, null=True)
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.SET_NULL)
    module = models.ForeignKey(Module, blank=True, null=True, on_delete=models.SET_NULL)
    cancel = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(populate_from='title', 
        default='',
        editable=False,
        unique=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = '-'.join((
                slugify(self.semester.semester),
                slugify(str(self.semester.year)),
                slugify(self.cl.title)
            ))
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "event"
        verbose_name_plural = "events"

    def __str__(self):
        return self.title

class Role(models.Model):
    participant = models.ForeignKey(Person, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ROLES = [
        ('D', 'Discussant'),
        ('M', 'Moderator'),
        ('P', 'Panelist'),
        ('L', 'Lecturer'),
        ('I', 'Introducer'),
        ('W', 'Workshop Leader')
    ]
    role = models.CharField(
        max_length=1,
        choices=ROLES,
        default='L',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "role"
        verbose_name_plural = "roles"
    
    def __str__(self):
        return self.role

class Days(models.Model):
    order = models.SmallIntegerField()
    day = models.CharField(max_length=10)
    abbrev = models.CharField(max_length=3)

    def __str__(self):
        return self.day