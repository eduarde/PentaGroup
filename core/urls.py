from django.conf.urls import url
from .views import Landing, Home

urlpatterns = [
    url(r'^$', Landing.as_view(), name='index'),
    url(r'^home/$', Home.as_view(), name='home'),
]