from flask import current_app, request, url_for
from flask_restful import Resource, abort


AS_CONTENT_TYPE = "application/ld+json; profile=\"https://www.w3.org/ns/activitystreams\""
API_CONTENT_HEADERS = {'Content-Type': AS_CONTENT_TYPE}
API_ACCEPT_HEADERS = {'Accept': AS_CONTENT_TYPE}

# specified by ActivityPub/ActivityStreams

VALID_CONTENT_TYPES = (
    "application/ld+json; profile=\"https://www.w3.org/ns/activitystreams\"",
    "application/ld+json; profile='https://www.w3.org/ns/activitystreams'",
    "application/activity+json",
)


def check_accept_headers(req):
    """
    """
    accept = req.headers.get('accept')
    if accept and (accept in VALID_CONTENT_TYPES):
        return True
    return False


def check_content_headers(req):
    """
    """
    content_type = request.headers.get('Content-Type')
    if content_type and (content_type in VALID_CONTENT_TYPES):
        return True
    return False


@current_app.before_request
def check_headers():
    """
    """
    if current_app.config['AP_STRICT_HEADERS'] and not check_accept_headers(request):
        abort(406)


class ActivityPubResource(Resource):
    """
    Base class for AP Resources
    """

    def __init__(self):
        super(ActivityPubResource, self).__init__()

        self.data_provider = None
        endpoint = getattr(self, "endpoint", None)
        if endpoint:
            self.data_provider = current_app.data_providers.get(endpoint)

    # @classmethod
    # def _post_url(cls, handle, post_number):
    #     return url_for("post", handle=handle, obj_id=post_number)

    # def activity_post(self, content, handle, to, cc, context=None):
    #     post_number = str(u['metrics']['post_count'])
    #     user_id = url_for("ap_user", handle=handle)

    #     post_id = ActivityPubResource._post_url(handle, post_number)
    #     post_url = ActivityPubResource._post_url(handle, post_number)

    #     # time = get_time()

    #     # could be string, bare object, or list/tuple
    #     if not isinstance(to, Iterable) or isinstance(to, basestring):
    #         to = [to]

    #     if not isinstance(cc, Iterable) or isinstance(cc, basestring):
    #         cc = [cc]

    #     create = vocab.Create(
    #         post_id,
    #         actor=vocab.Person(
    #             handle,
    #         ),
    #         to=to, cc=cc,
    #         object=vocab.Note(
    #             post_id,
    #             url=post_url,
    #             content=content))

    #     return create

    # def activity_person(self, uri_or_id, local=True, **kwargs):
    #     person_id = url_for(
    #         "ap_user", handle=uri_or_id
    #     ) if local else uri_or_id
    #     return vocab.Person(person_id, **kwargs)

    # def activity_follow(self, uri_or_id, local=True, **kwargs):
    #     person_id = url_for(
    #         "ap_follow", handle=uri_or_id
    #     ) if local else uri_or_id
    #     return vocab.Follow(person_id, **kwargs)

    # def get_object(self, handle, obj_id=None):
    #     """
    #     """
    #     raise NotImplementedError(
    #         "ActivityPubResource subclasses must implement get_object")

    # def get(self, handle, obj_id=None):
    #     """
    #     """
    #     if current_app.config['AP_STRICT_HEADERS'] and not self.check_accept_headers(request):
    #         abort(406)

    #     data = self.get_object(handle, obj_id=obj_id)

    #     return data


class ActivityPubCollection(ActivityPubResource):
    """
    Base class for AP collections
    """
    pass

class UserResource(ActivityPubResource):
    """
    User endpoint
    """
    endpoint = "user"

    # /<string:handle>
    def get(self, handle):
        uri = url_for("ap_user", handle=handle)

        if self.data_provider:
            user = self.data_provider.get_object(handle)

        return user


class FollowingCollection(ActivityPubCollection):
    """
    Following endpoint
    """
    endpoint = "following"

    # /<string:handle>/following
    def get(self, handle):
        """
        GET handler
        """
        following = []
        if self.data_provider:
            following = self.data_provider.get_objects(handle)
        return following
