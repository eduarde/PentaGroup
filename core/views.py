from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView, DetailView
from .models import Category, Group, Member, Post
from actstream.models import Action, Follow, following

# Create your views here.
class Landing(View):
    template_name = 'core/index.html'

    def get(self, request):
        return render(request, self.template_name)



class Home(ListView):
    model = Action
    template_name = 'core/home.html'
    context_object_name = 'actions'

    def get_recent_groups(self):
        return Group.objects.all().order_by('-created_date') 

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['groups'] = self.get_recent_groups()
        return context

    def get_queryset(self_queryset):
         return Action.objects.all();



class Notifications(ListView):
    model = Action
    template_name = 'core/notifications.html'
    context_object_name = 'actions'

    def get_queryset(self_queryset):
        return Action.objects.all();



class Explore(ListView):
    model = Category
    template_name = 'core/explore.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.all()




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

    def get_object(self):
         return get_object_or_404(Post, pk=self.kwargs.get("pk"))
