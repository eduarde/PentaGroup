from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from actstream.managers import ActionManager, stream

# This file is the time stamp manager that creates and returns action generated time.
# Additional return other parameters than time.

class CoreActionManager(ActionManager):
    
    @stream
    def corestream(self, obj, verb='posted', time=None):
        if time is None:
            time = datetime.now()

        return obj.actor_actions.filter(verb = verb, timestap__lte = time)

