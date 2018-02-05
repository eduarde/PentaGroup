from django.test import TestCase
from .models import Category, Group, Post
from django.contrib.auth.models import User
from actstream.actions import is_following
from actstream.models import Action
from django.test.client import Client
from .helper import ActionVerb

class GroupTestCase(TestCase):

    def setUp(self):
        
        self.user = User.objects.create_user('myuser', 'myuser@test.com', 'passTest')
        self.c = Client()
        self.c.login(username=self.user.username, password=self.user.password)
        self.category = Category.objects.create(title='CategoryTest')


    def test_do_follow_actions(self):
        group = Group.objects.create(admin=self.user, title="GroupTest", category_ref=self.category, description="Group test follow actions")
        group.do_follow_actions()
        self.assertTrue(is_following(self.user,group))
        self.assertTrue(Action.objects.get(verb=ActionVerb.CREATE))



class PostTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('myuser', 'myuser@test.com', 'passTest')
        self.c = Client()
        self.c.login(username=self.user.username, password=self.user.password)
        self.category = Category.objects.create(title='CategoryTest')
        self.group = Group.objects.create(admin=self.user, title="GroupTest", category_ref=self.category, description="Group test follow actions")
    
    def test_do_actions(self):
        post = Post.objects.create(author=self.user, group_ref = self.group, title="Post Test", text="Text Post Test")
        post.do_actions()
        self.assertTrue(Action.objects.get(verb=ActionVerb.PUBLISH))
    

