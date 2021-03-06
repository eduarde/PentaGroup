
from django.apps import AppConfig


# This apps.py registers the models to the action manager.In order to use activity stream we need to register our models first.
# So I am registering my User model with dashboard models Group, Post.

class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        from actstream import registry
        registry.register(self.get_model('Member')) #actor
        registry.register(self.get_model('Group'))  # object / target
        registry.register(self.get_model('Post'))    # object 
        registry.register(self.get_model('Category'))  # target
