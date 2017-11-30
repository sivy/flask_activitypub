import logging

# from activipy import vocab
from activipy.demos import dbm
from flask import Flask

import data_providers
from flask_activitypub import ActivityPub

logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger(__name__)


app = Flask("test app")

app.config['DB'] = "example.db"
setattr(
    app, "env", dbm.DbmEnv)
setattr(
    app, "db", dbm.JsonDBM.open(app.config["DB"]))

ap_app = ActivityPub(app)


ap_app.add_data_provider(
    "following", data_providers.FollowingProvider)

app.run()
