# coding: utf-8

import flask
import auth
import model
import util
import config
import wtforms
from flask.ext import wtf
from main import app

class TrackUpdateForm(wtf.Form):

  album = wtforms.StringField('Album', filters=[util.strip_filter])
  title = wtforms.StringField('Title', filters=[util.strip_filter])
  artist = wtforms.StringField('Artist', filters=[util.strip_filter])
  albumartist = wtforms.StringField('Album Artist', filters=[util.strip_filter])
  originaldate = wtforms.StringField('Original Date', filters=[util.strip_filter])
  composer = wtforms.StringField('Composer', filters=[util.strip_filter])
  lyricist = wtforms.StringField('Lyricist', filters=[util.strip_filter])
  writer = wtforms.StringField('Writer', filters=[util.strip_filter])
  totaltracks = wtforms.IntegerField('Total Tracks')
  discnumber = wtforms.IntegerField('Disc Number')
  genre = wtforms.SelectMultipleField('Genre', choices=[(t, t.title()) for t in model.Track.genre._choices],default="unknown")
  mood = wtforms.SelectMultipleField('Mood', choices=[(t, t.title()) for t in model.Track.genre._choices],default="Okay")
  rating = wtforms.IntegerField('Rating')
  musicbrainz_recordingid = wtforms.StringField('musicbrainz_recordingid', filters=[util.strip_filter])
  musicbrainz_trackid = wtforms.StringField('musicbrainz_trackid', filters=[util.strip_filter])
  musicbrainz_albumid = wtforms.StringField('musicbrainz_albumid', filters=[util.strip_filter])
  musicbrainz_artistid = wtforms.StringField('musicbrainz_artistid', filters=[util.strip_filter])
  musicbrainz_albumartistid = wtforms.StringField('musicbrainz_albumartistid', filters=[util.strip_filter])
  language = wtforms.StringField('language', filters=[util.strip_filter])
  website = wtforms.StringField('website', filters=[util.strip_filter])
  stream_url = wtforms.StringField('stream_url', filters=[util.strip_filter])

###############################################################################
# Tracks List
###############################################################################
@app.route('/track/')
@auth.login_required
def track_list():
  track_dbs, track_cursor = model.Track.get_dbs(
      # user_key=auth.current_user_key(),
    )

  return flask.render_template(
      'track/track_list.html',
      html_class='track-list',
      title='Track List',
      track_dbs=track_dbs,
      next_url=util.generate_next_url(track_cursor),
    )
###############################################################################
# Tracks Create
###############################################################################  
@app.route('/track/create/', methods=['GET', 'POST'])
@auth.login_required
def track_create():
  form = TrackUpdateForm()
  if form.validate_on_submit():
    track_db = model.Track()

    form.populate_obj(track_db)
    track_db.put()
    return flask.redirect('/track/%i' % track_db.key.id())
  return flask.render_template(
      '/track/track_update.html',
      html_class='track-create',
      title='Create Track',
      form=form,
    )
###############################################################################
# Tracks View
###############################################################################
@app.route('/track/<int:track_id>/')
@auth.login_required
def track_view(track_id):
  track_db = model.Track.get_by_id(track_id)
  # if not track_db or track_db.user_key != auth.current_user_key():
  #   flask.abort(404)
  return flask.render_template(
      'track/track_view.html',
      html_class='track-view',
      title=track_db.title,
      track_db=track_db,
    )

###############################################################################
# Tracks Update
###############################################################################
@app.route('/track/<int:track_id>/update/', methods=['GET', 'POST'])
@auth.login_required
def track_update(track_id):
  track_db = model.Track.get_by_id(track_id)
  # if not track_db or track_db.user_key != auth.current_user_key():
  #   flask.abort(404)
  form = TrackUpdateForm(obj=track_db)
  if form.validate_on_submit():
    form.populate_obj(track_db)
    track_db.put()
    return flask.redirect(flask.url_for('track_list', order='-modified'))
  return flask.render_template(
      'track/track_update.html',
      html_class='track-update',
      title=track_db.title,
      form=form,
      track_db=track_db,
    )