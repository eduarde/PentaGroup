from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Category, Group, Member, Post
from django.utils.decorators import method_decorator
from .custom_decorators import follow_decorator, follow_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse
from .forms import GroupForm, PostForm, PostGroupForm, PostDeleteForm
from actstream import action
from actstream.models import Action, Follow, following, followers
from actstream.actions import is_following, follow, unfollow
from .helper import FollowMethod, ActionVerb
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

# Create your views here.
class Landing(View):
    template_name = 'core/index.html'

    def get(self, request):
        return render(request, self.template_name)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse_lazy('home'))
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})




class Home(ListView):
    model = Action
    template_name = 'core/home.html'
    context_object_name = 'actions'
    queryset = Action.objects.all().order_by('-id')[:15]

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
        return following(self.request.user.pk, Group)




class ExpandGroup(ListView):
    model = Post
    template_name = 'core/posts.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super(ExpandGroup, self).get_context_data(**kwargs)
        context['group'] = self.get_group_object()
        context['users'] = self.get_followers()
        return context

    def get_followers(self):
        return followers(self.get_group_object())

    def get_group_object(self):
        return get_object_or_404(Group, pk=self.kwargs.get("pk"))

    def get_user(self):
        return self.request.user    

    # @follow_required(raise_exception=False)
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
        follow(self.request.user, group_obj) if FollowMethod.FOLLOW.value == int(self.kwargs.get('action')) else unfollow(self.request.user, group_obj)
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

  

class CreatePost(CreateView):

    model = Post
    template_name = 'core/create_post.html'
    success_url = reverse_lazy('home')
    form_class = PostForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.user)
        return render(request, self.template_name, {'post_form': form,  'title': 'Add a new post'})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.user, request.POST)
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.author = self.request.user
            self.object.save()
            form.save()
            return HttpResponseRedirect(self.success_url)



class CreatePostGroup(CreateView):

    model = Post
    template_name = 'core/create_post.html'
    form_class = PostGroupForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'post_form': form, 'title': 'Add a new post'})

    def get_group_object(self):
        return get_object_or_404(Group, pk=self.kwargs.get("pk"))

    def get_success_url(self, **kwargs):         
            return reverse('expand-group', kwargs={'pk': self.kwargs.get("pk")})
        
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.author = self.request.user
            self.object.group_ref = self.get_group_object()
            self.object.save()
            form.save()
            return HttpResponseRedirect(self.get_success_url())
    


class EditPost(UpdateView):

    template_name = 'core/create_post.html'
    form_class = PostGroupForm

    def get_object(self):
        return get_object_or_404(Post, pk=self.kwargs.get('pk'))

    def get_group_object(self, group_pk):
        return get_object_or_404(Group, pk=group_pk)

    def get_success_url(self, **kwargs):         
            return reverse('expand-group', kwargs={'pk': self.get_object().group_ref.pk })

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(instance=self.object)
        return render(request, self.template_name, {'post_form': form, 'title': 'Edit post'})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        if form.is_valid():
            self.object = form.save(commit=True)
            self.object.save()
            return HttpResponseRedirect(self.get_success_url())   


class DeletePost(DeleteView):

    template_name = 'core/delete_post.html'
    form_class = PostDeleteForm
    
    def get_group(self):
        return self.get_object().group_ref

    def get_object(self):
        return get_object_or_404(Post, pk=self.kwargs.get('pk'))
    
    def get_success_url(self, **kwargs):         
            return reverse('expand-group', kwargs={'pk': self.group.pk })

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(instance=self.object)
        return render(request, self.template_name, {'post_form': form})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.group = self.get_group()
        form = self.form_class(request.POST, instance=self.object)
        if form.is_valid():
            self.object.delete()
            return HttpResponseRedirect(self.get_success_url())  



class FavoritePost(View):

    def get(self, request, *args, **kwargs):
        post_obj = get_object_or_404(Post, pk=self.kwargs.get("pk"))
        follow(self.request.user, post_obj, send_action=False) if FollowMethod.ADDED_FAV.value == int(self.kwargs.get('action')) else unfollow(self.request.user, post_obj, send_action=False)
        return HttpResponseRedirect(reverse('expand-group', kwargs={'pk': post_obj.group_ref.pk}))



class Favorites(ListView):
    model = following
    template_name = 'core/favorites.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return following(self.request.user.pk, Post)