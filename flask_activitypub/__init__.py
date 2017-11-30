"""
Totally hacked up proof of concept
"""

from flask import request, url_for, current_app
from flask_restful import Api, Resource, abort
from activipy import vocab
from collections import Iterable
from flask_activitypub.resources import (
    UserResource, FollowingCollection)

# from functools import wraps


class ActivityPubProvider(object):
    """
    ABC for data providers
    """
    pass


class ActivityPub(object):
    """
    """
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app, strict_headers=False):
        """
        """
        self.app.config['AP_STRICT_HEADERS'] = strict_headers

        self.activity_pub_api = Api(app)

        self.data_providers = {}

        self.activity_pub_api.add_resource(
            UserResource, "/user/<string:handle>",
            endpoint="ap_user")

        self.activity_pub_api.add_resource(
            FollowingCollection, "/user/<string:handle>/following",
            endpoint="ap_following")


        # app.add_resource("/<str:handle>inbox", self.inbox)
        # app.add_resource("/<str:handle>/outbox", self.outbox)
        # app.add_resource("/<str:handle>/following", self.following)
        # app.add_resource("/<str:handle>/followers", self.followers)
        # app.add_resource("/<str:handle>/likes", self.likes)

        # if hasattr(app, 'teardown_appcontext'):
        #     app.teardown_appcontext(self.teardown)
        # else:
        #     app.teardown_request(self.teardown)

    # define a decorator factory that creates a decorator
    # that can wrap a function and return
    # def add_resource(self, endpoint, path, cls):
    #     """
    #     - Lookup Resource subclass in self.handler_classes
    #     - Or, create Resource subclass for endpoint
    #     - Add func as method
    #     """
    #     endpoint_key = "ap_%s" % endpoint

    #     if endpoint_key in self.app.view_functions.keys():
    #         del self.app.view_functions[endpoint_key]

    #     self.activity_pub_api.add_resource(
    #         cls, path, endpoint=endpoint_key)

    def add_data_provider(self, endpoint, cls):
        self.data_providers[endpoint] = cls

    def user_handler(self, cls):
        self.add_handler(
            "user", "/<string:handle>", cls)

    def post_handler(self, cls):
        self.add_handler(
            "post", '/user/<string:handle>/<obj_id>', cls)

    def following_handler(self, cls):
        self.add_handler(
            "following", "/<string:handle>/following", cls)

    def outbox_handler(self, cls):
        self.add_handler(
            "outbox", '/<string:handle>/outbox', cls)

    def inbox_handler(self, cls):
        self.add_handler(
            "inbox", '/<string:handle>/inbox', cls)

    def followers_handler(self, cls):
        self.add_handler(
            "followers", '/<str:handle>/followers', cls)

    def liked_handler(self, cls):
        self.add_handler(
            "liked", '/<str:handle>/likes', cls)
