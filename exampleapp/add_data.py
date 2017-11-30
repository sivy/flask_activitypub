from exampleapp.app import app
from activipy.demos import dbm
from activipy.vocab import (
    Person, Note, Follow, Like)

env = dbm.DbmEnv
db = dbm.JsonDBM.open(app.config["DB"])

for uid in range(0,6):
    dbm.dbm_save(Person(
        "/"
    ))