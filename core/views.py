from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView, DetailView, TemplateView
from django.views.generic.edit import UpdateView
from .models import Category, Group, Member, Post
from actstream.models import Action, Follow, following
from actstream.actions import is_following, follow, unfollow
from django.utils.decorators import method_decorator
from .custom_decorators import follow_decorator, FollowAction, follow_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse
from .forms import GroupForm
from django.views.generic.edit import CreateView
from actstream import action

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

    def get_context_data(self, **kwargs):
        context = super(ExpandGroup, self).get_context_data(**kwargs)
        context['group'] = self.get_group_object()
        return context

    def get_group_object(self):
        return get_object_or_404(Group, pk=self.kwargs.get("pk"))

    def get_user(self):
        return self.request.user    

    @follow_required(raise_exception=False)
    def get_queryset(self):
        return Post.objects.all().filter(group_ref = self.get_group_object()).order_by('-published_date')



class ExpandPost(DetailView):
    model = Post
    template_name = 'core/post.html'
    context_object_name = 'post'    
    
    def get_user(self):
        return self.request.user

    @follow_required(raise_exception=True)
    def get_object(self):
        return get_object_or_404(Post, pk=self.kwargs.get("pk"))





class FollowGroup(View):
    
    def get(self, request, *args, **kwargs):
        group_obj = get_object_or_404(Group, pk=self.kwargs.get("pk"))
        follow(self.request.user, group_obj)
      
        return HttpResponseRedirect(reverse('expand-group', kwargs={'pk':group_obj.pk}))



class CreateGroup(CreateView):

    model = Group
    template_name = 'core/create_group.html'
    success_url = reverse_lazy('home') 
    form_class = GroupForm

    def get(self, request, *args, **kwargs):	
        form = self.form_class()
        return render(request, self.template_name, {'group_form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.admin = self.request.user
            self.object.save()
            form.save()
            return HttpResponseRedirect(self.success_url)

  
    

   
