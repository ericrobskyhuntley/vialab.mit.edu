from django.db import models
from cal.models import Semester, Days
from tutorials.models import Skill, Software
from people.models import Person, Institution
from martor.models import MartorField

import os

from django.template.defaultfilters import slugify

class SessionTime(models.Model):
    days = models.ManyToManyField(Days)
    start = models.TimeField()
    end = models.TimeField()

    def __str__(self):
        return str(list(self.days.all())) + ' ' + str(self.start) + '-' + str(self.end)

class Class(models.Model):
    title = models.CharField(max_length=100)
    number = models.CharField(max_length=15)
    ug = models.BooleanField(default=False)
    grad = models.BooleanField(default=False)
    units = models.CharField(max_length=15)
    prereqs = models.CharField(max_length=100, blank=True, null=True)
    institution = models.ForeignKey(Institution, blank=True, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
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
        verbose_name = "class"
        verbose_name_plural = "classes"

    def __str__(self):
        return self.title

def banner_filename(instance, filename):
    path = 'images/banners/'
    fname, fext = os.path.splitext(filename)
    format = instance.slug + fext
    return os.path.join(path, format)

def syllabus_filename(instance, filename):
    path = 'syllabi/'
    fname, fext = os.path.splitext(filename)
    format = instance.slug + fext
    return os.path.join(path, format)

class ClassInstance(models.Model):
    cl = models.ForeignKey(Class, null=True, on_delete=models.CASCADE, related_name='instance')
    semester = models.ForeignKey(Semester, blank=True, null=True, on_delete=models.CASCADE)
    desc = MartorField(max_length=2000, blank=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    instructors = models.ManyToManyField(Person, through='InstructorOrder')
    sessions = models.ManyToManyField(SessionTime, through='SessionType', blank=True)
    canvas = models.URLField(max_length=200)
    dept_site = models.URLField(max_length=200)
    banner = models.ImageField(null=True, blank=True, upload_to = banner_filename)
    software = models.ManyToManyField(Software, blank=True)
    skills = models.ManyToManyField(Skill, blank=True)
    syllabus = models.FileField(blank=True, default='', upload_to = syllabus_filename)
    slug = models.SlugField(
        default='',
        editable=False,
        unique=True
    )

    class Meta:
        verbose_name = "class instance"
        verbose_name_plural = "class instances"

    def __str__(self):
        return self.cl.title + ' ' + self.semester.semester + ' ' + str(self.semester.start.year)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = '-'.join((
                slugify(self.semester.semester),
                slugify(str(self.semester.year)),
                slugify(self.cl.title)
            ))
        super().save(*args, **kwargs)

class SessionType(models.Model):
    class_instance = models.ForeignKey(ClassInstance, null=True, on_delete=models.CASCADE, related_name='session_type')
    session_time = models.ForeignKey(SessionTime, on_delete=models.CASCADE, related_name='session_type')
    FORM = [
        ('L', 'Lecture'),
        ('B', 'Lab'),
        ('D', 'Discussion'),
        ('R', 'Recitation'),
    ]
    form = models.CharField(max_length=1,
        choices=FORM,
        default='L'
    )

    class Meta:
        verbose_name = "session"
        verbose_name_plural = "sessions"

    def __str__(self):
        return self.class_instance.cl.title + self.form

class InstructorOrder(models.Model):
    class_instance = models.ForeignKey(ClassInstance, null=True, on_delete=models.CASCADE, related_name='instructor_order')
    instructor = models.ForeignKey(Person, null=True, on_delete=models.CASCADE, related_name='instructor_order')
    order = models.SmallIntegerField(null=True)
    # def __str__(self):
        # return self.class_instance.cl.title + '/' + self.instructor