from django.conf.urls import url
from .views import Landing, Home, Explore

urlpatterns = [
    url(r'^$', Landing.as_view(), name='index'),
    url(r'^home/$', Home.as_view(), name='home'),
    url(r'^explore/$', Explore.as_view(), name='explore'),
]