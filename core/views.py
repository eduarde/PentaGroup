from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView, DetailView, TemplateView
from .models import Category, Group, Member, Post
from actstream.models import Action, Follow, following
from actstream.actions import is_following, follow, unfollow
from django.utils.decorators import method_decorator
from .custom_decorators import follow_decorator, FollowAction, follow_required
from django.contrib.auth.models import User

# Create your views here.
class Landing(View):
    template_name = 'core/index.html'

    def get(self, request):
        return render(request, self.template_name)



class Home(ListView):
    model = Action
    template_name = 'core/home.html'
    context_object_name = 'actions'
    queryset = Action.objects.all()

    def get_recent_groups(self):
        return Group.objects.all().order_by('-created_date') 

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['groups'] = self.get_recent_groups()
        return context



class Explore(ListView):
    model = Category
    template_name = 'core/explore.html'
    context_object_name = 'categories'
    queryset = Category.objects.all()

  


class ExploreGroups(ListView):
    model = Group
    template_name = 'core/explore-groups.html'
    context_object_name = 'groups'

    def get_object(self):
        return get_object_or_404(Category, pk=self.kwargs.get("pk"))

    def get_queryset(self):
        return Group.objects.all().filter(category_ref = self.get_object())




class FollowingGroups(ListView):
    model = following
    template_name = 'core/following.html'
    context_object_name = 'groups'

    def get_queryset(self):
        return following(self.request.user.pk)




class ExpandGroup(ListView):
    model = Post
    template_name = 'core/posts.html'
    context_object_name = 'posts'

    def get_object(self):
        return get_object_or_404(Group, pk=self.kwargs.get("pk"))

    def get_queryset(self):
        return Post.objects.all().filter(group_ref = self.get_object()).order_by('-published_date')



class ExpandPost(DetailView):
    model = Post
    template_name = 'core/post.html'
    context_object_name = 'post'
    
    def get_user(self):
        return self.request.user

    @follow_required('core/home.html')
    def get_object(self):
        return get_object_or_404(Post, pk=self.kwargs.get("pk"))



#TODO: make ajax call or something 
# class FollowGroup(ExpandGroup):

#     @follow_decorator(FollowAction.UNFOLLOW)
#     def get(self, request, *args, **kwargs):
#         return super(FollowGroup, self).get(request, args, kwargs)
  
    

   
