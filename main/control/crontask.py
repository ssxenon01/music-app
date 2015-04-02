from requests.exceptions import ConnectionError

from model.track import Track


__author__ = 'Gundsambuu'

from apiclient.discovery import build
import httplib2
import config
from oauth2client.appengine import AppAssertionCredentials
from main import app
import api.sons
import time
from oauth2client.client import SignedJwtAssertionCredentials
import discogs_client
from api.pyItunes import Library

d = discogs_client.Client('Music/0.1')
d._base_url = 'https://api.discogs.com'
d.per_page = 1

sons_network = api.sons.SonsNetwork()

if (config.DEVELOPMENT):
    client_email = '121688381876-hj5hs4oohukagfep7hqq64iljtn3i0kf@developer.gserviceaccount.com'
    with open("Music.pem") as f:
        private_key = f.read()
    credentials = SignedJwtAssertionCredentials(client_email, private_key, 'https://www.googleapis.com/auth/drive')
else:
    credentials = AppAssertionCredentials(scope='https://www.googleapis.com/auth/drive')

@app.route('/tasks/gdrive')
def cron_task_gdrive():
    http = credentials.authorize(httplib2.Http(timeout=60))
    service = build("drive", "v2", http=http, developerKey="listen-fm@appspot.gserviceaccount.com")

    param = {}
    param['q'] = 'mimeType contains "audio" and starred=false'
    param['maxResults'] = 1000
    page_token = None
    last_call_time = 0
    l = Library("iTunes Music Library.xml")

    itunes_songs = l.songs

    while True:
        if page_token:
            param['pageToken'] = page_token
        files = service.files().list(**param).execute()
        page_token = files.get('nextPageToken')
        for item in files['items']:
            file_name = item['title'].replace('.%s' % item['fileExtension'], '')
            # Adding delay cuz of Discogs Rate-Limit
            DELAY_TIME = 1 # time between each request must more that 1 second in order to avoid 60 request per minute
            now = time.time()

            time_since_last = now - last_call_time

            if time_since_last < DELAY_TIME:
                time.sleep(DELAY_TIME - time_since_last)

            last_call_time = now
            if file_name.isdigit():
                track_db = Track.query(Track.sons_id == file_name).get()
                if track_db is None:
                    track_db = Track(sons_id=file_name)
                track_db.gdrive_id = item['id']
                itunes_song = itunes_songs[file_name]
                if itunes_song is not None:
                    track_db.genre = itunes_song.genre
                    track_db.duration = itunes_song.total_time

                sons_track = sons_network.get_track(file_name)
                if 'default' not in sons_track.image:
                    track_db.cover_img = 'http://sons.mn/' + sons_track.image.replace('/uploads/',
                                                                                      'image-cache/w300-h300-c/')
                else:
                    track_db.cover_img = 'http://sons.mn' + sons_track.image

                track_db.album = sons_track.album_name
                track_db.title = sons_track.title
                track_db.artist = sons_track.artist_name
                track_db.origin = 'Mongolian'

                track_db.put()
                if not config.DEVELOPMENT:
                    service.files().update(fileId=item['id'], body={'labels.starred': True}).execute()
            elif ' - ' in file_name:
                try:
                    title, artist = file_name.split(' - ', 1)

                    discog_result = d.search('', title=title, artist=artist.replace('.', ' '),
                                             token="mhkqGGqAxmkGFOlbnWRRQZYcqDLxLianrCocIIJE", type="Release", per_page=1)

                    if len(discog_result) > 0:
                        discog_release = discog_result[0]
                        if isinstance(discog_result[0], discogs_client.Master):
                            discog_release = discog_result[0].main_release
                        track_db = Track.query().filter(Track.gdrive_id == item['id']).get()
                        if track_db is None:
                            track_db = Track(gdrive_id=item['id'])
                        track_db.title = discog_release.title
                        track_db.year = str(discog_release.year)
                        track_db.cover_img = discog_release.thumb
                        track_db.genre = ','.join(discog_release.genres)
                        if len(discog_release.artists) > 0:
                            track_db.artist = discog_release.artists[0].name
                        track_db.put()
                        if not config.DEVELOPMENT:
                            service.files().update(fileId=item['id'], body={'labels.starred': True}).execute()
                except ConnectionError:
                    pass
        if not page_token:
            break
    return 'Ok'


# @app.route('/tasks/collect')
# def collect():
#     url = "http://www.billboard.com/rss/charts/hot-100"
#     result = urlfetch.fetch(url)
#     if result.status_code == 200:
#         xml = ElementTree.fromstring(result.content)
#
#         for item in xml.iterfind('channel/item'):
#             if (model.Track.query(model.Track.title == item.find('chart_item_title').text,
#                                   model.Track.artist == item.find('artist').text).count(limit=1) == 0):
#                 track_db = model.Track(
#                     title=item.find('chart_item_title').text,
#                     artist=item.find('artist').text
#                 )
#                 track_db.put()
#             logging.info(item.find('title').text)
#         return str(xml.findtext(".//title"))