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
    albumartist = ndb.StringProperty()
    originaldate = ndb.StringProperty()
    composer = ndb.StringProperty()
    lyricist = ndb.StringProperty()
    writer = ndb.StringProperty()
    tracknumber = ndb.IntegerProperty(default=0)
    totaltracks = ndb.IntegerProperty(default=0)
    discnumber = ndb.IntegerProperty(default=0)
    genre = ndb.StringProperty()
    mood = ndb.StringProperty(repeated=True, choices=[
        'Accepted', 'Accomplished', 'Aggravated', 'Alone', 'Amused', 'Angry', 'Annoyed', 'Anxious', 'Apathetic',
        'Ashamed', 'Awake', 'Bewildered',
        'Bitchy', 'Bittersweet', 'Blah', 'Blank', 'Blissful', 'Bored', 'Bouncy', 'Calm', 'Cheerful', 'Chipper', 'Cold',
        'Complacent', 'Confused',
        'Content', 'Cranky', 'Crappy', 'Crazy', 'Crushed', 'Curious', 'Cynical', 'Dark', 'Depressed', 'Determined',
        'Devious', 'Dirty', 'Disappointed',
        'Discontent', 'Ditzy', 'Dorky', 'Drained', 'Drunk', 'Ecstatic', 'Energetic', 'Enraged', 'Enthralled', 'Envious',
        'Exanimate', 'Excited',
        'Exhausted', 'Flirty', 'Frustrated', 'Full', 'Geeky', 'Giddy', 'Giggly', 'Gloomy', 'Good', 'Grateful', 'Groggy',
        'Grumpy', 'Guilty', 'Happy',
        'High', 'Hopeful', 'Hot', 'Hungry', 'Hyper', 'Impressed', 'Indescribable', 'Indifferent', 'Infuriated', 'Irate',
        'Irritated', 'Jealous',
        'Jubilant', 'Lazy', 'Lethargic', 'Listless', 'Lonely', 'Loved', 'Mad', 'Melancholy', 'Mellow', 'Mischievous',
        'Moody', 'Morose', 'Naughty',
        'Nerdy', 'Not', 'Specified\'Numb', 'Okay', 'Optimistic', 'Peaceful', 'Pessimistic', 'Pissed', 'off\'Pleased',
        'Predatory', 'Quixotic',
        'Recumbent', 'Refreshed', 'Rejected', 'Rejuvenated', 'Relaxed', 'Relieved', 'Restless', 'Rushed', 'Sad',
        'Satisfied', 'Shocked', 'Sick', 'Silly',
        'Sleepy', 'Smart', 'Stressed', 'Surprised', 'Sympathetic', 'Thankful', 'Tired', 'Touched', 'Uncomfortable',
        'Weird'
    ])
    rating = ndb.IntegerProperty()
    musicbrainz_recordingid = ndb.StringProperty(default='')
    musicbrainz_trackid = ndb.StringProperty(default='')
    musicbrainz_albumid = ndb.StringProperty(default='')
    musicbrainz_artistid = ndb.StringProperty(default='')
    musicbrainz_albumartistid = ndb.StringProperty(default='')
    gdrive_id = ndb.StringProperty(default='')
    gdrive_etag = ndb.StringProperty(default='')
    language = ndb.StringProperty(default='')
    website = ndb.StringProperty(default='')
    stream_url = ndb.StringProperty(default='')
    cover_img = ndb.StringProperty(default='')

    FIELDS = {
        'album': fields.String,
        'title': fields.String,
        'artist': fields.List(fields.String),
        'albumartist': fields.String,
        'originaldate': fields.String,
        'composer': fields.String,
        'lyricist': fields.List(fields.String),
        'mood': fields.List(fields.String),
        'writer': fields.String,
        'totaltracks': fields.String,
        'discnumber': fields.String,
        'genre': fields.String,
        'rating': fields.String,
        'musicbrainz_recordingid': fields.String,
        'musicbrainz_trackid': fields.String,
        'musicbrainz_albumid': fields.String,
        'musicbrainz_artistid': fields.String,
        'musicbrainz_albumartistid': fields.String,
        'language': fields.String,
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



    FIELDS.update(model.Base.FIELDS)
