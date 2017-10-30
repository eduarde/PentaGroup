from django.shortcuts import render
from django.views.generic import View

# Create your views here.
class Landing(View):
    template_name = 'core/index.html'

    def get(self, request):
        return render(request, self.template_name)



class Home(View):
    template_name = 'core/home.html'

    def get(self, request):
        return render(request, self.template_name)




class Explore(View):
    template_name = 'core/explore.html'

    def get(self, request):
        return render(request, self.template_name)