# coding: utf-8

import flask
import logging
import config
import model
from google.appengine.api import urlfetch
from xml.etree import ElementTree
from main import app
from musicbrainz2.webservice import Query, TrackFilter, WebServiceError
import pylast

# from oauth2client.client import SignedJwtAssertionCredentials

API_KEY = "8c57be12c08c3586cc46d3609d7f83e8" # this is a sample key
API_SECRET = "0e3f2355e220957076f386a8eb884b01"
network = pylast.LastFMNetwork(api_key = API_KEY, api_secret =
    API_SECRET)

###############################################################################
# Welcome
###############################################################################
@app.route('/')
def welcome():
  return flask.render_template('welcome.html', html_class='welcome')

@app.route('/genres')
def genres():
  return flask.render_template('genres.html', html_class='genres')


###############################################################################
# Sitemap stuff
###############################################################################
@app.route('/sitemap.xml')
def sitemap():
  response = flask.make_response(flask.render_template(
      'sitemap.xml',
      lastmod=config.CURRENT_VERSION_DATE.strftime('%Y-%m-%d'),
    ))
  response.headers['Content-Type'] = 'application/xml'
  return response


###############################################################################
# Warmup request
###############################################################################
@app.route('/_ah/warmup')
def warmup():
  # TODO: put your warmup code here
  return 'success'


@app.route('/collect')
def collect():
	url = "http://www.billboard.com/rss/charts/hot-100"
	result = urlfetch.fetch(url)
	if result.status_code == 200:
		xml = ElementTree.fromstring(result.content)
		
		for item in xml.iterfind('channel/item'):
			if(model.Track.query(model.Track.title==item.find('chart_item_title').text, model.Track.artist==item.find('artist').text).count(limit=1)==0):
				track_db = model.Track(
					title=item.find('chart_item_title').text,
					artist=item.find('artist').text
					)
				track_db.put()
			logging.info(item.find('title').text)
		return str(xml.findtext(".//title"))

@app.route('/collectdata')
def collectdata():
	track_dbs = model.Track.query(model.Track.musicbrainz_trackid == '')
	for track_db in track_dbs:
		try:
			track = network.get_track(track_db.artist,track_db.title)
			album = track.get_album()
			if(album):
				track_db.album = album.title
				track_db.musicbrainz_albumid = album.get_mbid()
			track_db.musicbrainz_trackid = track.get_mbid()
			logging.info('mbid: %s' % track.get_mbid() )
			# for tag in track.get_top_tags():
				# logging.info(tag.item.name)
			track_db.put()
		except Exception, e:
			logging.info(' error : %s' % e.details)
	return "total "

