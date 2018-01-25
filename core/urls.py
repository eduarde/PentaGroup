from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required, permission_required
from .views import Landing, Home, Explore, ExploreGroups, FollowingGroups, ExpandGroup, Notifications

urlpatterns = [
    url(r'^$', Landing.as_view(), name='index'),
    url(r'^login/$', auth_views.login, name='login'),

    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),

    url(r'^home/$', login_required(Home.as_view()), name='home'),

    url(r'^explore/$', login_required(Explore.as_view()), name='explore'),
    url(r'^explore/groups/(?P<pk>\d+)$', ExploreGroups.as_view(), name='explore-groups'),

    url(r'^following/$', login_required(FollowingGroups.as_view()), name='following'),
    url(r'^following/groups/(?P<pk>\d+)$', login_required(ExpandGroup.as_view()), name='expand-group'),

    url(r'^notifications/$', login_required(Notifications.as_view()), name='notifications'),
    
]