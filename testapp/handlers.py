import logging

from flask_activitypub import (
    ActivityPub, ActivityPubResource, ActivityPubCollection)

from activipy.demos import dbm

db = dbm.JsonDBM.open("../social.db")
env = dbm.DbmEnv

logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger(__name__)


def db_fetch(uri):
    if uri in db:
        return db[uri]
    return None


class UserResource(ActivityPubResource):
    """
    Resource returning a representation of a 
    User
    """
    def get_object(self, handle, obj_id=None):
        # user = storage.get_user_by_handle(handle)
        LOG.debug("UserResource.get_object: %s", handle)
        user = db_fetch()

        # return self.activity_person(
        #     handle, local=True).json()


class PostResource(ActivityPubResource):
    """
    Resource returning a representation of a 
    Post
    """
    def get_object(self, handle, obj_id=None):
        # user = storage.get_user_by_handle(handle)
        # post = storage.get_post(post_id)
        # return self.activity_post(
        #    post.content, handle, post.to, post.cc).json()
        return {}


class FollowingResource(ActivityPubCollection):
    """
    Resource returning a representation of a 
    Follow
    """
    def get_objects(self, handle):
        # user = storage.get_user_by_handle(handle)
        # return [
        #     self.create_follow(handle, follow.id) for 
        #     follow in user.following]
        return []