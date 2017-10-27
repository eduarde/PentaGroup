from django.db import models
from django.utils import timezone
from datetime import date, timedelta




class UserProfile(models.Model):
    FEMALE = 'Female'
    MALE = 'Male'

    GENDER_CHOICES = (
        (FEMALE, 'Female'),
        (MALE, 'Male')
    )

    user = models.ForeignKey('auth.User', unique=True, on_delete=models.CASCADE)
    gender = models.CharField(max_length=200, choices=GENDER_CHOICES, default=FEMALE)
    dob = models.DateField('Date of Birth', null=True)
    
    def __str__(self):
        return "Profile " + self.user.username




class Group(models.Model):
    admin = models.ForeignKey('auth.User')
    title = models.CharField('Title', max_length=200)
    description = models.TextField('Description')
    members = models.ManyToManyField(UserProfile, related_name='members')
    created_date = models.DateTimeField('Created', blank=True, null=True)
    private = models.BooleanField(default=True)

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