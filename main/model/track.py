# coding: utf-8

from __future__ import absolute_import

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
    genre = ndb.StringProperty(repeated=True, choices=[
        'Alternative', 'Alternative Rock', 'College Rock', 'Experimental Rock', 'Goth Rock', 'Grunge', 'Hardcore Punk',
        'Hard Rock', 'Indie Rock',
        'New Wave', 'Progressive Rock', 'Punk', 'Shoegaze', 'Steampunk', 'Anime', 'Blues', 'Acoustic Blues',
        'Chicago Blues', 'Classic Blues',
        'Contemporary Blues', 'Country Blues', 'Delta Blues', 'Electric Blues', 'Children’s Music', 'Lullabies',
        'Sing-Along', 'Stories',
        'Classical', 'Avant-Garde', 'Baroque', 'Chamber Music', 'Chant', 'Choral', 'Classical Crossover', 'Early Music',
        'High Classical',
        'Impressionist', 'Medieval', 'Minimalism', 'Modern Composition', 'Opera', 'Orchestral', 'Renaissance',
        'Romantic', 'Wedding Music',
        'Comedy', 'Novelty', 'Standup Comedy', 'Country', 'Alternative Country', 'Americana', 'Bluegrass',
        'Contemporary Bluegrass',
        'Contemporary Country', 'Country Gospel', 'Honky Tonk', 'Outlaw Country', 'Traditional Bluegrass',
        'Traditional Country',
        'Urban Cowboy', 'Dance / EMD', 'Breakbeat', 'Dubstep', 'Exercise', 'Garage', 'Hardcore', 'Hard Dance',
        'Hi-NRG / Eurodance',
        'House', 'Jackin House', 'Jungle/Drum’n\'bass', 'Techno', 'Trance', 'Disney', 'Easy Listening', 'Bop', 'Lounge',
        'Swing',
        'Electronic', 'Ambient', 'Crunk', 'Downtempo', 'Electro', 'Electronica', 'Electronic Rock', 'IDM/Experimental',
        'Industrial',
        'Enka', 'French Pop', 'German Folk', 'German Pop', 'Fitness & Workout', 'Hip-Hop/Rap', 'Alternative Rap',
        'Bounce', 'Dirty South',
        'East Coast Rap', 'Gangsta Rap', 'Hardcore Rap', 'Hip-Hop', 'Latin Rap', 'Old School Rap', 'Rap',
        'Underground Rap', 'West Coast Rap',
        'Holiday', 'Chanukah', 'Christmas', 'Christmas: Children’s', 'Christmas: Classic', 'Christmas: Classical',
        'Christmas: Jazz',
        'Christmas: Modern', 'Christmas: Pop', 'Christmas: R&B', 'Christmas: Religious', 'Christmas: Rock', 'Easter',
        'Halloween',
        'Holiday: Other', 'Thanksgiving', 'Indie Pop', 'Industrial', 'Inspirational – Christian & Gospel', 'CCM',
        'Christian Metal',
        'Christian Pop', 'Christian Rap', 'Christian Rock', 'Classic Christian', 'Contemporary Gospel', 'Gospel',
        'Christian & Gospel',
        'Praise & Worship', 'Qawwali', 'Southern Gospel', 'Traditional Gospel', 'Instrumental', 'March (Marching Band)',
        'J-Pop', 'J-Rock',
        'J-Synth', 'J-Ska', 'J-Punk', 'Jazz', 'Acid Jazz (with thx to Hunter', 'lson)', 'Avant-Garde Jazz', 'Big Band',
        'Blue Note',
        'Contemporary Jazz', 'Cool', 'Crossover Jazz', 'Dixieland', 'Ethio-jazz', 'Fusion', 'Hard Bop', 'Latin Jazz',
        'Mainstream Jazz',
        'Ragtime', 'Smooth Jazz', 'Trad Jazz', 'K-Pop', 'Karaoke', 'Kayokyoku', 'Latino', 'Alternativo & Rock Latino',
        'Baladas y Boleros',
        'Brazilian', 'Contemporary Latin', 'Latin Jazz', 'Pop Latino', 'Raíces', 'Reggaeton y Hip-Hop',
        'Regional Mexicano', 'Salsa y Tropical',
        'New Age', 'Environmental', 'Healing', 'Meditation', 'Nature', 'Relaxation', 'Travel', 'Opera', 'Pop',
        'Adult Contemporary', 'Britpop',
        'Pop/Rock', 'Soft Rock', 'Teen Pop', 'R&B/Soul', 'Contemporary R&B', 'Disco', 'Doo Wop', 'Funk', 'Motown',
        'Neo-Soul', 'Quiet Storm', 'Soul',
        'Reggae', 'Dancehall', 'Dub', 'Roots Reggae', 'Ska', 'Rock', 'Adult Alternative', 'American Trad Rock',
        'Arena Rock', 'Blues-Rock',
        'British Invasion', 'Death Metal/Black Metal', 'Glam Rock', 'Hair Metal', 'Hard Rock', 'Metal', 'Jam Bands',
        'Prog-Rock/Art Rock',
        'Psychedelic', 'Rock & Roll', 'Rockabilly', 'Roots Rock', 'Singer/Songwriter', 'Southern Rock', 'Surf',
        'Tex-Mex', 'Singer/Songwriter',
        'Alternative Folk', 'Contemporary Folk', 'Contemporary Singer/Songwriter', 'Folk-Rock', 'New Acoustic',
        'Traditional Folk', 'Soundtrack',
        'Foreign Cinema', 'Musicals', 'Original Score', 'Soundtrack', 'TV Soundtrack', 'Spoken Word',
        'Tex-Mex / Tejano', 'Chicano', 'Classic',
        'Conjunto', 'Conjunto Progressive', 'New Mex', 'Tex-Mex', 'Vocal', 'Barbershop', 'Doo-wop', 'Standards',
        'Traditional Pop', 'Vocal Jazz',
        'Vocal Pop', 'World', 'Africa', 'Afro-Beat', 'Afro-Pop', 'Asia', 'Australia', 'Bossa Nova', 'Cajun',
        'Caribbean', 'Celtic', 'Celtic Folk',
        'Contemporary Celtic', 'Drinking Songs', 'Drone', 'Europe', 'France', 'Hawaii', 'Indian Pop', 'Japan',
        'Japanese Pop', 'Klezmer',
        'Middle East', 'North America', 'Polka', 'South Africa', 'South America', 'Traditional Celtic', 'Worldbeat',
        'Zydeco', 'Mongolian Long Song', 'Mongolian Zohiol'
    ])
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
    language = ndb.StringProperty(default='')
    website = ndb.StringProperty(default='')
    stream_url = ndb.StringProperty(default='')

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
    }

    FIELDS.update(model.Base.FIELDS)
