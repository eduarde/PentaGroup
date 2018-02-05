from django import forms

from .models import Group, Post

class GroupForm(forms.ModelForm):

    class Meta:
        model = Group
        exclude = ('admin', 'created_date')



class PostForm(forms.ModelForm):

    class Meta:
        model = Post      
        exclude = ('author', 'published_date')