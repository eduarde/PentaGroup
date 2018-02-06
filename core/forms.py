from django import forms

from .models import Group, Post
from actstream.models import following

class GroupForm(forms.ModelForm):

    class Meta:
        model = Group
        exclude = ('admin', 'created_date')



class PostForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['group_ref'].queryset = Group.objects.filter(pk__in=[x.pk for x in following(user)]) 

    class Meta:
        model = Post      
        exclude = ('author', 'published_date')


class PostGroupForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('author', 'published_date', 'group_ref')