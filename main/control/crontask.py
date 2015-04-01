from pylast import WSError
from model.track import Track

__author__ = 'Gundsambuu'

from apiclient.discovery import build
import httplib2
import logging
import config
import model
from oauth2client.appengine import AppAssertionCredentials
from google.appengine.api import urlfetch, memcache
from xml.etree import ElementTree
from main import app
import pylast
from oauth2client.client import SignedJwtAssertionCredentials
import discogs_client
import api.sons

API_KEY = "8c57be12c08c3586cc46d3609d7f83e8"  # this is a sample key
API_SECRET = "0e3f2355e220957076f386a8eb884b01"
network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)
d = discogs_client.Client('Music/0.1')
d._base_url = 'https://api.discogs.com'

sons_network = api.sons.SonsNetwork()
sons_network.enable_caching()


@app.route('/discogs')
def discogs():
    results = d.search('', title='Uptown Funk', artist="Bruno Mars", token="mhkqGGqAxmkGFOlbnWRRQZYcqDLxLianrCocIIJE",
                       type="Artist")

    return str(results[0].artists[0].name)


@app.route('/cron_task_gdrive')
def cron_task_gdrive():
    credentials = None

    if (config.DEVELOPMENT):
        client_email = '121688381876-hj5hs4oohukagfep7hqq64iljtn3i0kf@developer.gserviceaccount.com'
        with open("Music.pem") as f:
            private_key = f.read()
        credentials = SignedJwtAssertionCredentials(client_email, private_key, 'https://www.googleapis.com/auth/drive')
    else:
        credentials = AppAssertionCredentials(scope='https://www.googleapis.com/auth/drive')

    http = credentials.authorize(httplib2.Http(memcache))
    service = build("drive", "v2", http=http, developerKey="listen-fm@appspot.gserviceaccount.com")
    param = {}
    param['q'] = 'modifiedDate >= "2015-03-22T12:00:00-08:00" and mimeType contains "audio"'
    files = service.files().list(**param).execute()
    for item in files['items']:
        stream_url = 'https://drive.google.com/uc?id=%s' % item['id']
        array = item['title'].replace('.%s' % item['fileExtension'], '').split('-')
        if model.Track.query(model.Track.gdrive_id == item['id']).count(limit=1) == 0:
            track_db = model.Track(
                title=array[0],
                artist=array[1],
                stream_url=stream_url,
                gdrive_id=item['id'],
                gdrive_etag=item['etag']
            )
            fill_track_db(track_db)
        else:
            track_db = model.Track.query(model.Track.gdrive_id == item['id']).get()
            track_db.title = array[0]
            track_db.artist = array[1]
            fill_track_db(track_db)

    return 'ok'


@app.route('/cron_task_gdrive_mgl')
def cron_task_gdrive_mgl():
    credentials = None

    if (config.DEVELOPMENT):
        client_email = '121688381876-hj5hs4oohukagfep7hqq64iljtn3i0kf@developer.gserviceaccount.com'
        with open("Music.pem") as f:
            private_key = f.read()
        credentials = SignedJwtAssertionCredentials(client_email, private_key, 'https://www.googleapis.com/auth/drive')
    else:
        credentials = AppAssertionCredentials(scope='https://www.googleapis.com/auth/drive')

    http = credentials.authorize(httplib2.Http(memcache))
    service = build("drive", "v2", http=http, developerKey="listen-fm@appspot.gserviceaccount.com")
    param = {}
    param['q'] = 'mimeType contains "audio"'
    # param['maxResults'] = 500
    page_token = None
    while True:
        if page_token:
            param['pageToken'] = page_token
        files = service.files().list(**param).execute()
        page_token = files.get('nextPageToken')
        for item in files['items']:
            file_name = item['title'].replace('.%s' % item['fileExtension'], '')
            if file_name.isdigit():
                logging.info(file_name)
                sons_track = sons_network.get_track(file_name)
                track_db = Track.query(Track.artist == sons_track.artist_name and Track.title == sons_track.title).get()
                if track_db is None:
                    track_db = Track(title=sons_track.title, artist=sons_track.artist_name, album=sons_track.album_name,
                                    gdrive_id=item['id'], language="Mongolian")
                if 'default' not in sons_track.image:
                    track_db.cover_img = 'http://sons.mn/'+sons_track.image.replace('/uploads/', 'image-cache/w300-h300-c/')
                else:
                    track_db.cover_img = 'http://sons.mn'+sons_track.image
                track_db.gdrive_id = item['id']
                track_db.put()
        if not page_token:
            break
    return 'Ok'


def fill_track_db(track_db):
    track = network.get_track(track_db.artist, track_db.title)
    try:
        if track.get_mbid():
            album = track.get_album()
            if album:
                track_db.album = album.title
                track_db.musicbrainz_albumid = album.get_mbid()
                track_db.cover_img = track.get_album().get_cover_image(3)
                logging.info('Cover Image Album: %s' % track_db.cover_img)
            track_db.musicbrainz_trackid = track.get_mbid()

            artist = track.get_artist()
            if artist and model.Artist.query(model.Artist.mbid == artist.get_mbid()).count(limit=1) == 0:
                artist_db = model.Artist(
                    name=artist.name,
                    mbid=artist.get_mbid(),
                    image_url=artist.get_cover_image(3)
                )
                logging.info('Cover Image Artist: %s' % artist_db.image_url)
                if track_db.cover_img is None or track_db.cover_img == '':
                    track_db.cover_img = artist.get_cover_image(3)
                artist_db.put()
        track_db.put()
    except WSError:
        logging.error('error')
        track_db.put()


@app.route('/tasks/collect')
def collect():
    url = "http://www.billboard.com/rss/charts/hot-100"
    result = urlfetch.fetch(url)
    if result.status_code == 200:
        xml = ElementTree.fromstring(result.content)

        for item in xml.iterfind('channel/item'):
            if (model.Track.query(model.Track.title == item.find('chart_item_title').text,
                                  model.Track.artist == item.find('artist').text).count(limit=1) == 0):
                track_db = model.Track(
                    title=item.find('chart_item_title').text,
                    artist=item.find('artist').text
                )
                track_db.put()
            logging.info(item.find('title').text)
        return str(xml.findtext(".//title"))


@app.route('/tasks/collectdata')
def collectdata():
    track_dbs = model.Track.query()
    counter = 0
    for track_db in track_dbs:
        try:
            track = network.get_track(track_db.artist, track_db.title)
            if track.get_mbid():
                album = track.get_album()
                if album:
                    track_db.album = album.title
                    track_db.musicbrainz_albumid = album.get_mbid()
                    track_db.cover_img = track.get_album().get_cover_image(3)
                track_db.musicbrainz_trackid = track.get_mbid()
                track_db.put()
                artist = track.get_artist()
                if artist:
                    if model.Artist.query(model.Artist.mbid == artist.get_mbid()).count(limit=1) == 0:
                        artist_db = model.Artist(
                            name=artist.name,
                            mbid=artist.get_mbid(),
                            image_url=artist.get_cover_image(3)
                        )
                        artist_db.put()

        except WSError, e:
            logging.info(' error : %s' % e.details)
    return "total %i" % counter
