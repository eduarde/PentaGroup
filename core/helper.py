from enum import Enum 

class ActionVerb(Enum):

    ADDED = "added"
    CREATED = "created"
    POSTED = "posted"
    PUBLISHED = "published"



class FollowMethod(Enum):
    FOLLOW = 1
    UNFOLLOW = 0
    ADDED_FAV = 1
    REMOVE_FAV = 0