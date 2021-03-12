from django.db import models
from martor.models import MartorField
from django.db.models import Prefetch
from people.models import Person
from reading.models import ReadingList
import time
import os

def banner_filename(instance, filename):
    path = 'images/banners/'
    fname, fext = os.path.splitext(filename)
    format = instance.title.replace(' ', '-').replace('.', '').replace(',','').lower() + '_' + str(round(time.time())) + fext
    return os.path.join(path, format)

def icon_filename(instance, filename):
    path = 'images/icons'
    fname, fext = os.path.splitext(filename)
    format = instance.name.replace(' ', '-').lower() + '_' + str(round(time.time())) + fext
    return os.path.join(path, format)

class TutorialsMetadata(models.Model):
    app_name = models.CharField(max_length=25)
    app_desc = MartorField(max_length=1000, blank=True)
    modules_name = models.CharField(max_length=25)
    modules_desc = MartorField(max_length=1000, blank=True)
    series_name = models.CharField(max_length=25)
    series_desc = MartorField(max_length=1000, blank=True)
    episode_name = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "tutorials metadata"
        verbose_name_plural = "tutorials metadata"

    def __str__(self):
        return self.app_name

class Series(models.Model):
    title = models.CharField(max_length=100)
    desc = MartorField(max_length=2000, blank=True)
    banner = models.ImageField(null=True, blank=True, upload_to = banner_filename)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=False)

    @property
    def author_list(self):
        modules = Module.objects.filter(series = self.pk)
        return Person.objects.filter(module__id__in = modules.values_list('id', flat=True)).distinct().order_by('last')

    @property
    def episode_list(self):
        return Module.objects.filter(series = self.pk).distinct().order_by('episode__number')

    @property
    def software_list(self):
        modules = Module.objects.filter(series = self.pk)
        return Software.objects.filter(module__id__in = modules.values_list('id', flat=True)).distinct().order_by('name')
    
    @property
    def skill_list(self):
        modules = Module.objects.filter(series = self.pk)
        return Skill.objects.filter(module__id__in = modules.values_list('id', flat=True)).distinct().order_by('name')
    
    @property
    def created(self):
        return self.history.earliest()

    @property
    def creator(self):
        return Person.objects.all().get(django_user=self.history.earliest().history_user)
    
    @property
    def modified(self):
        if self.history.latest().history_type == '+':
            return None
        else:
            return self.history.latest()

    @property
    def modifier(self):
        if self.history.latest().history_type == '+':
            return None
        else:
            return Person.objects.all().get(django_user=self.history.latest().history_user)

    class Meta:
        verbose_name = "series"
        verbose_name_plural = "series"

    def __str__(self):
        return self.title
    
class Software(models.Model):
    name = models.CharField(max_length=100)
    desc = MartorField(max_length=400)
    icon = models.ImageField(null=True, blank=True, upload_to = icon_filename)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "software"
        verbose_name_plural = "software"

    def __str__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(max_length=100)
    desc = MartorField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "skill"
        verbose_name_plural = "skills"

    def __str__(self):
        return self.name

class Module(models.Model):
    title = models.CharField(max_length=100)
    banner = models.ImageField(null=True, blank=True, upload_to = banner_filename)
    author = models.ManyToManyField(Person)
    software = models.ManyToManyField(Software, blank=True)
    skills = models.ManyToManyField(Skill, blank=True)
    series = models.ManyToManyField(Series, through='Episode', blank=True)
    desc = MartorField(max_length=1000, blank=True)
    body = MartorField(blank=True, default='')
    whatnext = MartorField(blank=True, default='')
    readings = models.ForeignKey(
        ReadingList, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL
    )
    materials = models.FileField(upload_to='uploads/%Y/%m/%d', blank=True, default='')
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    featured = models.BooleanField()
    slug = models.SlugField(
        default='',
        editable=True,
        unique=False
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = '-'.join((
                slugify(self.title),
            ))
        super().save(*args, **kwargs)

    @property
    def author_list(self):
        return Person.objects.filter(module__id=self.id)
    
    @property
    def software_list(self):
        return Software.objects.filter(module__id=self.id)
    
    @property
    def skill_list(self):
        return Skill.objects.filter(module__id=self.id)
    
    @property
    def created(self):
        return self.history.earliest()

    @property
    def creator(self):
        return Person.objects.all().get(django_user=self.history.earliest().history_user)
    
    @property
    def modified(self):
        if self.history.latest().history_type == '+':
            return None
        else:
            return self.history.latest()

    @property
    def modifier(self):
        if self.history.latest().history_type == '+':
            return None
        else:
            return Person.objects.all().get(django_user=self.history.latest().history_user)

    class Meta:
        verbose_name = "module"
        verbose_name_plural = "modules"

    def __str__(self):
        return self.title

class Episode(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "episode"
        verbose_name_plural = "episodes"

    def __str__(self):
        return self.module.title + self.series.title + str(self.number)