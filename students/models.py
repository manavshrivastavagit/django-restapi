from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

import os

from .validators import validate_date, validate_file_extension


def homework_material_filename(instance, filename):
    return os.path.join(
        'homework_materials',
        str(instance.clazz),
        str(instance.subject),
        filename
    )


class Class(models.Model):

    number = models.IntegerField(
        validators=[MinValueValidator(8), MaxValueValidator(12)],
        choices=[(i, i) for i in range(8, 13)],
    )
    letter = models.CharField(
        max_length=1,
        choices=[(l, l) for l in ['A', 'B', 'V', 'G']],
    )


    class Meta:
        ordering = ['number', 'letter']
        verbose_name_plural = 'classes'


    def __str__(self):
        return '{}{}'.format(self.number, self.letter)


class Student(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    clazz = models.ForeignKey(Class, on_delete=models.CASCADE)
    profile_image = models.ImageField(
        upload_to='images/', default='images/default.png'
    )
    info = models.TextField(max_length=2048, blank=True)


    def __str__(self):
        return '{} ({})'.format(self.user.username, self.clazz)


class Subject(models.Model):

    title = models.CharField(unique=True, max_length=50)


    class Meta:
        ordering = ['title']


    def __str__(self):
        return self.title


class Exam(models.Model):

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, validators=[validate_date])
    clazz = models.ForeignKey(Class, on_delete=models.CASCADE)
    topic = models.CharField(unique=True, max_length=60)
    details = models.TextField(max_length=1000, blank=True)


    class Meta:
        ordering = ['date', 'subject', 'clazz']


    def __str__(self):
        return '{} - {} ({})'.format(self.subject, self.clazz, self.date)


class News(models.Model):

    title = models.CharField(max_length=60, blank=False)
    content = models.TextField(max_length=1000, blank=False)
    author = models.ForeignKey(Student, on_delete=models.CASCADE)
    posted_on = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-posted_on']
        verbose_name_plural = 'news'
        unique_together = ('title', 'content')


    def __str__(self):
        return '{} ({})'.format(self.title, self.posted_on.date())


class Homework(models.Model):

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    clazz = models.ForeignKey(Class, on_delete=models.CASCADE)
    deadline = models.DateField(auto_now=False, validators=[validate_date])
    details = models.TextField(max_length=256, blank=True)
    materials = models.FileField(
        upload_to=homework_material_filename,
        blank=True,
        null=True,
        validators=[validate_file_extension]
    )


    class Meta:
        ordering = ['-deadline', 'clazz', 'subject']


    def __str__(self):
        return '{} ({}) - {}'.format(self.subject, self.clazz, self.deadline)


class Comment(models.Model):

    news = models.ForeignKey(News, on_delete=models.CASCADE)
    posted_by = models.ForeignKey(Student, on_delete=models.CASCADE)
    content = models.TextField(max_length=2048)
    posted_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return '{} - {}'.format(self.posted_by, self.news.title)
