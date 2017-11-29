# Flask-ActivityPub

Flask-ActivityPub is a Flask extension that should enable the developer to add social networking [ActivityPub](http://activitypub.rocks/) support to a Flask application. This could be the main purpose of the application, or could be implemented in a blueprint as a subsection (examples coming later).

It's WAY EARLY days and there is little code yet, though reading [testapp/app.py](./testapp/app.py) might be of use. Please Stand By.

## Design

Flask-ActivityPub is intended to provide the API endpoints and client functions to support federation with other social sites that implement the ActivityPub protocol. This will allow activity on the site to be shared with federated services.

```python
from flask import Flask
from flask_activitypub import ActivityPub

app = Flask("test app")

# configure application, blueprints, database, etc.

# add ActivityPub APIs
activity_app = ActivityPub(app)
```

This adds the ActivityPub extension, which provides a method for adding handlers for each ActivityPub endpoint:

```python
activity_app.follow_handler(FollowResource)
```

`FollowResource` is a subclass of `ActivityPubCollection`, a superclass provided by Flask-ActivityPub that does all request handling and data marshalling. Subclass handlers implement either `get_object` (for `ActivityPubResource` subclasses) or `get_objects` (for `ActivityPubCollection` subclasses).

```python

class FollowingResource(ActivityPubCollection):
    """
    Resource returning a representation of a 
    Follow
    """
    def get_objects(self, handle):
        user = storage.get_user_by_handle(handle)
        return [
            self.create_follow(handle, follow.id) for 
            follow in user.follow_collection]

```

### Acknowledgements

I've learned a lot of this from [Rowan](https://github.com/rowanlupton) esp from reading the [Smilodon](https://github.com/rowanlupton/smilodon) source code, tiny bits of which I've literally copied and pasted while trying to make things work. Additionally, I'm learning a lot from [Christian Webber](https://github.com/cwebber) and his ActivityStreams work with https://github.com/w3-social/activipy.

