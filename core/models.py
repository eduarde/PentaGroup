from django.db import models
from django.utils import timezone


class Group(models.Model):
    admin = models.ForeignKey('auth.User')
    title = models.CharField('Title', max_length=200)
    description = models.TextField('Description')
    created_date = models.DateTimeField('Created', blank=True, null=True)

    def create(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Post(models.Model):
    author = models.ForeignKey('auth.User')
    group_ref = models.ForeignKey('Group', null=True, verbose_name='Group')
    title = models.CharField('Title', max_length=200)
    text = models.TextField('Text')
    published_date = models.DateTimeField('Published', blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title