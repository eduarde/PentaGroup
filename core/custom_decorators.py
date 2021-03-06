from django.core.exceptions import PermissionDenied
from actstream.actions import is_following, follow, unfollow
from enum import Enum 
from functools import wraps


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



# Custom decorator to check if user has access to view posts from specific group

def follow_required(raise_exception=False):

    def decorator(view_func):

        @wraps(view_func)
        def _wrapped_view(request):

            result = view_func(request)
            try:
                # get the group from a single 'post' object
                group = result.group_ref
            except AttributeError:
                # get the group from the first 'post' obj from queryset
                group = result[0].group_ref

            user = request.get_user()

            if is_following(user, group):
                return result

            if raise_exception:
                raise PermissionDenied    
           
            return ""
    

        return _wrapped_view
    return decorator


