from flask import Flask
from flask_activitypub import ActivityPub, ActivityPubResource, ActivityPubCollection
from activipy import vocab

import handlers

import logging

app = Flask("test app")

ap_app = ActivityPub(app)

logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger(__name__)

ap_app.user_handler(handlers.UserResource)
ap_app.following_handler(handlers.FollowingResource)

app.run()
