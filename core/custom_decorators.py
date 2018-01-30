from django.core.exceptions import PermissionDenied
from actstream.actions import is_following, follow, unfollow
from enum import Enum 
from functools import wraps
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect

class FollowAction(Enum):
    FOLLOW = 1,
    UNFOLLOW = 2


def follow_decorator(action):

    def proceed(f):
        def wrap(*args, **kwargs):
            if action == FollowAction.FOLLOW:
                print('follow_object')
            elif action == FollowAction.UNFOLLOW:
                print('unfollow_object')
            return f(*args,**kwargs)
        return wrap
    return proceed



# Custom decorator to check if user has access 
# to view posts from specific group
# TODO: redirect to specific page if user is not following the group
def follow_required(redirect_url=None):

    def decorator(view_func):

        @wraps(view_func)
        def _wrapped_view(request):

            result = view_func(request)
            group = result.group_ref
            user = request.get_user()

            if is_following(user, group):
                return result
           
            return ""
            # return render_to_response(redirect_url)  

        return _wrapped_view
    return decorator


