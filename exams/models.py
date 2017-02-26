from django.db import models

from students.models import Class, Subject, Teacher

from exams.validators import validate_date


class Exam(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, validators=[validate_date])
    clazz = models.ForeignKey(Class, on_delete=models.CASCADE)
    topic = models.CharField(unique=True, max_length=60)
    details = models.TextField(max_length=1000, blank=True)
    author = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['date', 'subject', 'clazz']


    def __str__(self):
        return '{} - {} ({})'.format(self.subject, self.clazz, self.date)