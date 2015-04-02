# coding: utf-8

from __future__ import absolute_import
import json
from google.appengine.api import memcache

from google.appengine.ext import ndb

from api import fields
import model


class Track(model.Base):
    album = ndb.StringProperty()
    title = ndb.StringProperty()
    artist = ndb.StringProperty()
    origin = ndb.StringProperty()
    year = ndb.StringProperty()
    duration = ndb.IntegerProperty()
    composer = ndb.StringProperty()
    lyricist = ndb.StringProperty()
    writer = ndb.StringProperty()
    genre = ndb.StringProperty()
    mood = ndb.StringProperty()
    rating = ndb.IntegerProperty()
    musicbrainz_recordingid = ndb.StringProperty(default='')
    musicbrainz_trackid = ndb.StringProperty(default='')
    musicbrainz_albumid = ndb.StringProperty(default='')
    musicbrainz_artistid = ndb.StringProperty(default='')
    gdrive_id = ndb.StringProperty(default='')
    website = ndb.StringProperty(default='')
    stream_url = ndb.StringProperty(default='')
    cover_img = ndb.StringProperty(default='')
    sons_id = ndb.StringProperty()
    FIELDS = {
        'album': fields.String,
        'title': fields.String,
        'artist': fields.List(fields.String),
        'albumartist': fields.String,
        'originaldate': fields.String,
        'composer': fields.String,
        'mood': fields.List(fields.String),
        'totaltracks': fields.String,
        'discnumber': fields.String,
        'genre': fields.String,
        'rating': fields.String,
        'musicbrainz_recordingid': fields.String,
        'musicbrainz_trackid': fields.String,
        'musicbrainz_albumid': fields.String,
        'musicbrainz_artistid': fields.String,
        'musicbrainz_albumartistid': fields.String,
        'website': fields.String,
        'stream_url': fields.String,
        'cover_img': fields.String,
    }

    @staticmethod
    def genre_list():
        cached = memcache.get('genre.json')
        if cached is None:
            with open('genre.json') as data_file:
                data = json.load(data_file)
                memcache.set('genre.json', data)
                return data
        else:
            return cached

    def get_duration_time(self):
        if self.duration:
            m, s = divmod(int(self.duration)/1000, 60)
            return "%02d:%02d" % (m, s)
        else:
            return None

    FIELDS.update(model.Base.FIELDS)
