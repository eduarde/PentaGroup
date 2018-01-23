from django.conf.urls import url
from .views import Landing, Home, Explore, ExploreGroups, FollowingGroups, ExpandGroup

urlpatterns = [
    url(r'^$', Landing.as_view(), name='index'),
    url(r'^home/$', Home.as_view(), name='home'),

    url(r'^explore/$', Explore.as_view(), name='explore'),
    url(r'^explore/groups/(?P<pk>\d+)$', ExploreGroups.as_view(), name='explore-groups'),

    url(r'^following/$', FollowingGroups.as_view(), name='following'),
    url(r'^following/groups/(?P<pk>\d+)$', ExpandGroup.as_view(), name='expand-group'),


    
]