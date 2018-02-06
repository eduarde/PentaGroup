from django.db import models
from django.utils import timezone
from datetime import date, timedelta
from actstream.actions import is_following, follow, unfollow
from actstream import action
from .helper import ActionVerb



class Member(models.Model):
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
        return self.user.username



class Group(models.Model):
    admin = models.ForeignKey('auth.User')
    title = models.CharField('Title', max_length=200, help_text="Add a title for your desired group")
    image = models.ImageField('Image', upload_to = 'img/groups/', default = 'img/groups/default-img.gif', null=True)
    category_ref = models.ForeignKey('Category', null=True, help_text="Specify the category", verbose_name="Category")
    description = models.TextField('Description', help_text='Add a short description')
    created_date = models.DateTimeField('Created', blank=True, null=True)

    def do_follow_actions(self):
        action.send(self.admin, verb = ActionVerb.CREATED.value, action_object = self, target = self.category_ref)
        follow(self.admin, self)

    def save(self, *args, **kwargs):
        self.created_date = timezone.now()
        if self.id is None: 
            super(Group, self).save(*args, **kwargs)
            self.do_follow_actions()

    def __str__(self):
        return self.title



class Post(models.Model):
    author = models.ForeignKey('auth.User')
    group_ref = models.ForeignKey('Group', null=True, verbose_name='Group')
    title = models.CharField('Title', max_length=200)
    text = models.TextField('Text')
    published_date = models.DateTimeField('Published', blank=True, null=True)

    def do_actions(self):
        action.send(self.author, verb = ActionVerb.PUBLISHED.value, action_object = self, target = self.group_ref)

    def save(self, *args, **kwargs):
        self.published_date = timezone.now()
        if self.id is None: 
            super(Post, self).save(*args, **kwargs)  
            self.do_actions()  
        super(Post, self).save(*args, **kwargs) 

    def __repr__ (self):
        return '<Post: {} {}'.format(self.title, self.author)

    def __str__(self):
        return self.title



class Category(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to = 'img/categories/', default = 'img/categories/cake.png', null=True)

    def __str__(self):
        return self.title