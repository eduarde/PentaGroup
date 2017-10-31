from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView
from .models import Category, Group

# Create your views here.
class Landing(View):
    template_name = 'core/index.html'

    def get(self, request):
        return render(request, self.template_name)



class Home(View):
    template_name = 'core/home.html'

    def get(self, request):
        return render(request, self.template_name)




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