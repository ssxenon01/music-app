import logging
import urllib
import flask
from google.appengine.api import memcache
from google.appengine.ext import ndb
from jinja2._markupsafe import Markup
import model
from main import app
from model.track import Track

__author__ = 'Gundsambuu'

@app.route('/genres')
def genres():
    template = 'genres.html'
    if flask.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        template = 'genre_content.html'

    selected_genre = flask.request.args.get('type', '')
    genre_list = Track.genre_list()
    track_list = get_track_list_by_genre(selected_genre)

    return flask.render_template(template,
                                 html_class='genres',
                                 track_list=track_list,
                                 genre_list=genre_list,
                                 active=flask.request.args.get('type', ''))


def get_track_list_by_genre(genre):
    data = memcache.get('t_l_b_g'+genre)
    if data is not None:
        return data
    else:
        track_list = Track.query().filter(Track.genre == genre).fetch(limit=18)
        memcache.set('t_l_b_g'+genre, track_list, 60 * 60)
        return track_list


@app.template_filter('urlencode')
def urlencode_filter(s):
    if type(s) == 'Markup':
        s = s.unescape()
    s = s.encode('utf8')
    s = urllib.quote_plus(s)
    return Markup(s)