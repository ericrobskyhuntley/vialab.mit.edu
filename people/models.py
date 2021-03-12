from django.db import models
from django.contrib.auth.models import User
from django.utils.functional import cached_property
from martor.models import MartorField
from simple_history.models import HistoricalRecords
from autoslug import AutoSlugField
import os
import time

def photo_filename(instance, filename):
    path = 'images/personphotos'
    fname, fext = os.path.splitext(filename)
    f = '{0}-{1}'.format(instance.last, instance.first).replace(' ', '-').lower() + '_' + str(round(time.time())) + fext
    return os.path.join(path, f)

class PeopleMetadata(models.Model):
    name = models.CharField(max_length=25)
    desc = MartorField(max_length=1000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "people app metadata"
        verbose_name_plural = "people app metadata"

    def __str__(self):
        return self.name

class Institution(models.Model):
    dept = models.CharField(max_length=150, blank=True, null=True)
    inst = models.CharField(max_length=150)
    dept_website = models.CharField(max_length=200, blank=True, null=True)
    inst_website = models.CharField(max_length=200, blank=True, null=True)
    short = models.CharField(max_length=150, blank=True, null=True)
    abbr = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        verbose_name = "institution"
        verbose_name_plural = "institutions"

    def __str__(self):
        return self.dept

class Person(models.Model):
    photo = models.ImageField(null=True, blank=True, upload_to = photo_filename)
    first = models.CharField(max_length=25)
    middle = models.CharField(max_length=25, blank=True, default='')
    last = models.CharField(max_length=25)
    CREDS = [
        ('MCP', 'Master of City Planning'),
        ('PhD', 'Doctor of Philosophy'),
        ('MUP', 'Master of Urban Planning'),
        ('MURP', 'Master of Urban and Regional Planning'),
        ('MFA', 'Master of Fine Arts'),
        ('MLA', 'Master of Landscape Architecture'),
        ('MArch', 'Master of Architecture'),
        ('MBA', 'Master of Business Administration'),
        ('MPA', 'Master of Public Administration'),
        ('MDes', 'Master of Design Studies'),
        ('DDes', 'Doctor of Design'),
    ]
    cred = models.CharField(
        max_length = 5,
        choices = CREDS,
        default = 'PhD',
        null=True,
        blank=True
    )
    affil = models.ManyToManyField(Institution, through='Affiliation')
    email = models.EmailField(blank=True, default='')
    website = models.URLField(blank=True, default='')
    GENDERS = [
        ('M', 'He/him/his'),
        ('W', 'She/her/hers'),
        ('N', 'He/him/his or They/them/theirs'),
        ('H', 'She/her/hers or They/them/theirs'),
        ('T', 'They/them/theirs'),
    ]
    pronouns = models.CharField(
        max_length=1,
        choices=GENDERS,
        default='T',
    )
    TITLES = [
        ('D', 'Director'),
        ('A', 'Affiliate'),
        ('R', 'Research Assistant'),
        ('F', 'Faculty Steering Committee'),
        ('L', 'Alumni Board'),
    ]
    title = models.CharField(
        max_length=1,
        choices=TITLES,
        default='',
    )
    bio = MartorField(max_length=3000, blank=True)
    orcid = models.CharField(max_length=19, blank=True, default='')
    pgp = models.CharField(max_length=50, blank=True, default='')
    twitter = models.CharField(max_length=50, blank=True, default='')
    gitlab = models.CharField(max_length=25, blank=True, default='')
    github = models.CharField(max_length=25, blank=True, default='')
    zotero = models.CharField(max_length=25, blank=True, default='')
    linkedin = models.CharField(max_length=25, blank=True, default='')
    django_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    vita = models.FileField(upload_to='people/vitae/', blank=True, default='')
    slug = models.SlugField(
        default='',
        editable=True,
        unique=False
    )

    @property
    def full_name(self):
        """
        Returns full name.
        """
        return '%s %s %s' % (self.first, self.middle, self.last)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = '-'.join((
                slugify(self.first),
                slugify(self.middle),
                slugify(self.last),
            ))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "person"
        verbose_name_plural = "people"

    def __str__(self):
        return self.full_name

class Affiliation(models.Model):
    participant = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="affiliation")
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name="affiliation")
    primary = models.BooleanField(default=False)
    website = models.URLField(default='', blank=True)
    title = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.title