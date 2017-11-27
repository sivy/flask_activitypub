from flask import Flask
from flask_activitypub import ActivityPub, ActivityPubResource, ActivityPubCollection
from activipy import vocab

app = Flask("test app")

ap_app = ActivityPub(app)


class UserResource(ActivityPubResource):

    def get_object(self, handle):
        return vocab.Person(
            url_for("user", handle=handle)
        )

class FollowingResource(ActivityPubCollection):

    def get_objects(self, handle):
        return []


ap_app.following_handler(FollowingResource)

# app.run()