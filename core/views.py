from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView
from .models import Category, Group, Member, Post

# Create your views here.
class Landing(View):
    template_name = 'core/index.html'

    def get(self, request):
        return render(request, self.template_name)



class Home(ListView):
    model = Post
    template_name = 'core/home.html'
    context_object_name = 'posts'

    def get_recent_groups(self):
        return Group.objects.all().order_by('-created_date') 

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['groups'] = self.get_recent_groups()
        return context

    def get_queryset(self_queryset):
        return Post.objects.all().order_by('-published_date')




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

    def get_member(self):
        return Member.objects.get(user = self.request.user.pk)

    def get_queryset(self):
        return Group.objects.all().filter(category_ref = self.get_object()).exclude(members = self.get_member())




class FollowingGroups(ListView):
    model = Group
    template_name = 'core/following.html'
    context_object_name = 'groups'

    def get_member(self):
        return Member.objects.get(user = self.request.user.pk)

    def get_queryset(self):
        return Group.objects.filter(members = self.get_member())
    