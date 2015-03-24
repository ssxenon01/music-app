

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

API_KEY = "8c57be12c08c3586cc46d3609d7f83e8"  # this is a sample key
API_SECRET = "0e3f2355e220957076f386a8eb884b01"
network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)


@app.route('/tasks/gdrive')
def task_gdrive():
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
        logging.info(item['id'])
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
            track = network.get_track(track_db.artist, track_db.title)
            if track.get_mbid():
                album = track.get_album()
                if album:
                    track_db.album = album.title
                    track_db.musicbrainz_albumid = album.get_mbid()
                    track_db.cover_img = track.get_album().get_cover_image(3)
                track_db.musicbrainz_trackid = track.get_mbid()

                artist = track.get_artist()
                if artist:
                    if model.Artist.query(model.Artist.mbid == artist.get_mbid()).count(limit=1) == 0:
                        artist_db = model.Artist(
                            name=artist.name,
                            mbid=artist.get_mbid(),
                            image_url=artist.get_cover_image(3)
                        )
                        artist_db.put()
            track_db.put()

    return 'ok'




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
    track_dbs = model.Track.query(model.Track.musicbrainz_trackid == '')
    counter = 0
    for track_db in track_dbs:
        try:
            track = network.get_track(track_db.artist, track_db.title)
            if track.get_mbid():
                counter += 1
                album = track.get_album()
                if album:
                    track_db.album = album.title
                    track_db.musicbrainz_albumid = album.get_mbid()
                track_db.musicbrainz_trackid = track.get_mbid()
                logging.info('mbid: %s' % track.get_mbid())
                # for tag in track.get_top_tags():
                # logging.info(tag.item.name)
                track_db.put()
        except Exception, e:
            logging.info(' error : %s' % e.details)
    return "total %i" % counter
