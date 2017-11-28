"""
Totally hacked up proof of concept
"""

from flask import request, url_for, current_app
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

    def activity_post(self, content, handle, to, cc, context=None):
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
                post_id,
                url=post_url,
                content=content))

        return create

    def activity_person(self, uri_or_id, local=True, **kwargs):
        person_id = url_for(
            "ap_user", handle=uri_or_id
        ) if local else uri_or_id
        return vocab.Person(person_id, **kwargs)

    def activity_follow(self, uri_or_id, local=True, **kwargs):
        person_id = url_for(
            "ap_follow", handle=uri_or_id
        ) if local else uri_or_id
        return vocab.Follow(person_id, **kwargs)

    def get_object(self, handle, obj_id=None):
        """
        """
        raise NotImplementedError(
            "ActivityPubResource subclasses must implement get_object")

    def get(self, handle, obj_id=None):
        """
        """
        if current_app.config['AP_STRICT_HEADERS'] and not self.check_accept_headers(request):
            abort(406)
        
        data = self.get_object(handle, obj_id=obj_id)

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
        if current_app.config['AP_STRICT_HEADERS'] and not self.check_accept_headers(request):
            abort(400)
        
        data = self.get_objects(handle)

        return data


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

        self.handler_classes = {}

        self.activity_pub_api.add_resource(
            ActivityPubResource, "/user/<string:handle>",
            endpoint="ap_user")
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
        endpoint_key = "ap_%s" % endpoint
        
        if endpoint_key in self.app.view_functions.keys():
            del self.app.view_functions[endpoint_key]

        self.activity_pub_api.add_resource(
            cls, path, endpoint=endpoint_key)
    
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
