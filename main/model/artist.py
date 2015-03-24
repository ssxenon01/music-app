# coding: utf-8

from __future__ import absolute_import

from google.appengine.ext import ndb

from api import fields
import model


class Artist(model.Base):
    name = ndb.StringProperty()
    artist_type = ndb.StringProperty()
    gender = ndb.StringProperty(default='none', choices=['male', 'female', 'none'])
    mbid = ndb.StringProperty()
    website = ndb.StringProperty()
    image_url = ndb.StringProperty()

    FIELDS = {
        'name': fields.String,
        'artist_type': fields.String,
        'gender': fields.String,
        'mbid': fields.String,
        'website': fields.String,
        'image_url': fields.String,
    }

    FIELDS.update(model.Base.FIELDS)
