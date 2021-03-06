from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .views import Landing, Home, Explore, ExploreGroups, FollowingGroups, ExpandGroup, ExpandPost, FollowGroup, CreateGroup, CreatePost, CreatePostGroup, EditPost, DeletePost, FavoritePost, Favorites
from . import views

urlpatterns = [

    url(r'^$', Landing.as_view(), name='index'),
    
    url(r'^login/$', auth_views.login, name='login'),

    url(r'^signup/$', views.signup, name='signup'),

    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),

    url(r'^home/$', login_required(Home.as_view()), name='home'),

    url(r'^explore/$', login_required(Explore.as_view()), name='explore'),

    url(r'^explore/groups/(?P<pk>\d+)$', ExploreGroups.as_view(), name='expand-category'),

    url(r'^following/$', login_required(FollowingGroups.as_view()), name='following'),
    
    url(r'^group/(?P<pk>\d+)$', login_required(ExpandGroup.as_view()), name='expand-group'),
    
    url(r'^post/(?P<pk>\d+)$', login_required(ExpandPost.as_view()), name='expand-post'),

    url(r'^group/(?P<pk>\d+)/follow/(?P<action>\d+)$', login_required(FollowGroup.as_view()), name='follow'),

    url(r'^create/group/$', login_required(CreateGroup.as_view()), name='create-group'),

    url(r'^create/post/$', login_required(CreatePost.as_view()), name='create-post'),

    url(r'^create/post/(?P<pk>\d+)$', login_required(CreatePostGroup.as_view()), name='create-post-group'),

    url(r'^edit/post/(?P<pk>\d+)$', login_required(EditPost.as_view()), name='edit-post'),

    url(r'^delete/post/(?P<pk>\d+)$', login_required(DeletePost.as_view()), name='delete-post'),

    url(r'^post/(?P<pk>\d+)/fav/(?P<action>\d+)$', login_required(FavoritePost.as_view()), name='favorite'),

    url(r'^favorites/$', login_required(Favorites.as_view()), name='favorites'),


]