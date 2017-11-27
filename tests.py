from flask import Flask
from flask_activitypub import ActivityPub, ActivityPubResource, ActivityPubCollection
from activipy import vocab

app = Flask("test app")

ap_app = ActivityPub(app)


class UserResource(ActivityPubResource):

    def get_object(self, handle):
        # user = storage.get_user_by_handle(handle)
        return self.activity_person(handle, local=True).json()

class PostResource(ActivityPubResource):

    def get_object(self, handle, post_id):
        # user = storage.get_user_by_handle(handle)
        return self.activity_post(
            shandle, content, handle, to, cc, context=None).json()


class FollowingResource(ActivityPubCollection):

    def get_objects(self, handle):
        # user = storage.get_user_by_handle(handle)
        # return [
        #     self.create_follow(handle, follow.id) for 
        #     follow in user.following]
        return []


ap_app.user_handler(UserResource)
ap_app.following_handler(FollowingResource)

app.run()