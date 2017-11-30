from flask import current_app, url_for

from flask_activitypub import ActivityPubProvider

import activipy
from activipy import vocab


class AppProvider(ActivityPubProvider):

    def user_url(self, handle):
        return url_for("user", handle=handle)

    def post_url(self, handle, post_number):
        return url_for("post", handle=handle, post_number=post_number)


class FollowingProvider(AppProvider):
    """

    {
        "@context": "https://www.w3.org/ns/activitystreams",
        "summary": "Sally followed John",
        "type": "Follow",
        "actor": {
            "type": "Person",
            "name": "Sally"
        },
        "object": {
            "type": "Person",
            "name": "John"
        }
    }

    """

    def get_objects(self, handle):
        """
        Get the collection of user Follows
        """
        user = current_app.db.fetch(
            self.user_url(handle=handle))

        return vocab.OrderedCollection([
            vocab.Follow({
                "actor": user,
                "object": follow.object
            }) for follow in user.follow_collection])

    def get_object(self, handle, obj_id):
        """
        Get a single Follow by id
        """
        user = current_app.db.fetch(
            self.user_url(handle=handle))

        return vocab.Follow({
            "actor": user,
            "object": obj_id
        })

    # def create_object(self, handle, **kwargs):
    #     pass

    # def delete_object(self, handle, obj_id):
    #     pass

