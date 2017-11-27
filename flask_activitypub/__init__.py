"""
Totally hacked up proof of concept
"""

from flask import request, url_for
from flask_restful import Api, Resource, abort
from activipy import vocab
from collections import Iterable

# from functools import wraps


as_content_type = "application/ld+json; profile=\"https://www.w3.org/ns/activitystreams\""

API_CONTENT_HEADERS = {'Content-Type': as_content_type}
API_ACCEPT_HEADERS = {'Accept': as_content_type}

# specified by ActivityPub/ActivityStreams

VALID_CONTENT_TYPES = ( 
    "application/ld+json; profile=\"https://www.w3.org/ns/activitystreams\"", 
    "application/ld+json; profile='https://www.w3.org/ns/activitystreams'", 
    "application/activity+json")


class ActivityPubResource(Resource):
    """
    Base class for AP Resources
    """    

    def check_accept_headers(self, req):
        accept = req.headers.get('accept')
        if accept and (accept in VALID_CONTENT_TYPES):
            return True
        return False

    def check_content_headers(self, req):
        """
        """
        content_type = request.headers.get('Content-Type')
        if content_type and (content_type in VALID_CONTENT_TYPES):
            return True
        return False

    @classmethod
    def _post_url(cls, handle, post_number):
        return url_for("post", handle=handle, obj_id=post_number)

    def create_post(self, content, handle, to, cc, context=None):
        post_number = str(u['metrics']['post_count'])
        user_id = url_for("ap_user", handle=handle)

        post_id = ActivityPubResource._post_url(handle, post_number)
        post_url = ActivityPubResource._post_url(handle, post_number)
  
        # time = get_time()

        # could be string, bare object, or list/tuple
        if not isinstance(to, Iterable) or isinstance(to, basestring):
            to = [to]

        if not isinstance(cc, Iterable) or isinstance(cc, basestring):
            cc = [cc]

        create = vocab.Create(
            post_id,
            actor=vocab.Person(
                handle,
            ),
            to=to, cc=cc,
            object=vocab.Note(
                id,
                url=post_url,
                content=content))

        return create

    def create_person(self, uri_or_id, local=True, **kwargs):
        person_id = url_for(
            "ap_user", obj_id=uri_or_id
        ) if local else uri_or_id
        return vocab.Person(person_id, **kwargs)

    def get_object(self, handle, obj_id):
        """
        """
        raise NotImplementedError(
            "ActivityPubResource subclasses must implement get_object")

    def get(self, handle, obj_id):
        """
        """
        # if not self.check_accept_headers(request):
        #     abort(400)
        
        data = self.get_object(handle, obj_id)

        return data


class ActivityPubCollection(ActivityPubResource):
    """
    Base class for AP collections
    """

    def get_objects(self, handle):
        """
        """
        raise NotImplementedError(
            "ActivityPubCollection subclasses must implement get_objects")

    def get(self, handle):
        """
        """
        # if not self.check_accept_headers(request):
        #     abort(400)
        
        data = self.get_objects(handle)

        return data


class ActivityPub(object):
    """    
    """
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        """

        self.activity_pub_api = Api(app)

        self.handler_classes = {}

        # app.add_resource("/user/<str:handle>", self.user)
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
    def add_handler(self, endpoint, path, cls):
        """
        - Lookup Resource subclass in self.handler_classes
        - Or, create Resource subclass for endpoint
        - Add func as method
        """
        self.activity_pub_api.add_resource(
            cls, path, endpoint="ap_%s" % endpoint)
    
    # def user_handler(self, func):
    #     self.add_handler('user', '/user/<str:handle>', "get", func)

    # def post_user_handler(self, func):
    #     self.add_handler('/user/<str:handle>', "get", func)

    # def get_outbox(self, func):
    #     self.add_handler('/<str:handle>/outbox', "get", func)
    
    # def inbox(self):
    #     self.add_handler('/<str:handle>/inbox', method, cls)

    def following_handler(self, cls):
        self.add_handler(
            "following", "/<string:handle>/following", cls)
    
    # def followers(self):
    #     self.add_handler('/<str:handle>/followers', method, cls)
    
    # def likes(self):
    #     self.add_handler('/<str:handle>/likes', method, cls)

