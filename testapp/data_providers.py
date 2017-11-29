from flask_activitypub import ActivityPubProvider
from activipy import vocab

class FollowingProvider(ActivityPubProvider):
    """
    Resource returning a representation of a 
    Follow
    """
    def get_objects(self, handle):
        user = storage.get_user_by_handle(handle)
        return [
            {actor=user, object=follow.object} for 
            follow in user.follow_collection]

    def get_object(self, handle, obj_id):
        user = storage.get_user_by_handle(handle)
        return {actor=user, object=obj_id}

    def create_object(self, handle, **kwargs):
        user = storage.get_user_by_handle(handle)
        actor = kwargs.get("object")
        

    def delete_object(self, handle, obj_id):
        pass
