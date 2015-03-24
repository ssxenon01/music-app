__author__ = 'xenon'
# coding: utf-8

from google.appengine.ext import ndb

from api import fields
import model


class Album(model.Base):
    title = ndb.StringProperty()
    mbid = ndb.StringProperty()
    website = ndb.StringProperty()
    cover = ndb.StringProperty()
    artist_key = ndb.KeyProperty(kind=model.Artist)

    FIELDS = {
        'title': fields.String,
        'mbid': fields.String,
        'website': fields.String,
        'cover': fields.String,
    }

    FIELDS.update(model.Base.FIELDS)
