# coding: utf-8
import logging
import flask
from google.appengine.api import memcache
import config
import model
from main import app


# ##############################################################################
# Welcome
# ##############################################################################


@app.route('/')
def welcome():
    discover_list = get_discover_list()
    new_songs = get_new_songs()

    return flask.render_template('welcome.html',
                                 html_class='welcome',
                                 discover_list=discover_list,
                                 new_songs=new_songs
                                 )


def get_new_songs():
    data = memcache.get('get_new_songs')
    if data is not None:
        logging.info('from cache')
        return data
    else:
        data = model.Track.query().order(model.Track.created).fetch(limit=8)
        memcache.add('key', data, 60)
        return data


def get_discover_list():
    data = memcache.get('get_discover_list')
    if data is not None:
        return data
    else:
        data = model.Track.query(model.Track.musicbrainz_trackid != ''
                                 and model.Track.stream_url != "").fetch(limit=10)
        memcache.add('key', data, 60)
        return data


@app.route('/genres')
def genres():
    return flask.render_template('genres.html', html_class='genres')


# ##############################################################################
# Sitemap stuff
# ##############################################################################
@app.route('/sitemap.xml')
def sitemap():
    response = flask.make_response(flask.render_template(
        'sitemap.xml',
        lastmod=config.CURRENT_VERSION_DATE.strftime('%Y-%m-%d'),
    ))
    response.headers['Content-Type'] = 'application/xml'
    return response


# ##############################################################################
# Warmup request
# ##############################################################################
@app.route('/_ah/warmup')
def warmup():
    # TODO: put your warmup code here
    return 'success'
