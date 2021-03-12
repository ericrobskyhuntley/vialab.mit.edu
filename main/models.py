from django.db import models
from martor.models import MartorField
from simple_history.models import HistoricalRecords
from people.models import Person, Institution
import time

def vid_filename(instance, filename):
    path = 'videos'
    fname, fext = os.path.splitext(filename)
    f = 'feature_' + str(round(time.time())) + fext
    return os.path.join(path, f)

class MainMetadata(models.Model):
    main_name = models.CharField(max_length=50, blank=False)
    short_desc = models.CharField(max_length=400, blank=False)
    about_name = models.CharField(max_length=20, blank=False)
    institution = models.ForeignKey(Institution, blank=True, null=True, on_delete=models.SET_NULL)
    about = MartorField(max_length=2000, blank=False)
    address = MartorField(max_length=2000, blank=False)
    email = models.EmailField(blank=True, default='')
    twitter = models.CharField(max_length=50, blank=True, default='')
    gitlab = models.CharField(max_length=25, blank=True, default='')
    github = models.CharField(max_length=25, blank=True, default='')
    zotero = models.CharField(max_length=25, blank=True, default='')
    feature_vid = models.FileField(blank=True, default='', upload_to = vid_filename)
    colophon_name = models.CharField(max_length=25, null=True, blank=True, default='')
    colophon = MartorField(max_length=12000, null=True, blank=True, default='')
    linkedin = models.CharField(max_length=25, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    # @property
    # def about_formatted(self):
    #     return markdownify(self.about)
    
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
        verbose_name = "main app metadata"
        verbose_name_plural = "main app metadata"

    def __str__(self):
        return self.main_name