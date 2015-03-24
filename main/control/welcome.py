# coding: utf-8
import flask
import config
import model
from main import app


# ##############################################################################
# Welcome
# ##############################################################################


@app.route('/')
def welcome():
    discover_list = model.Track.query(model.Track.musicbrainz_trackid != '' and model.Track.stream_url != "")
    new_songs = model.Track.query().order(model.Track.created).fetch(limit=8)
    return flask.render_template('welcome.html',
                                 html_class='welcome',
                                 discover_list=discover_list,
                                 new_songs=new_songs
                                 )


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
