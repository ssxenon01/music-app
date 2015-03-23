# coding: utf-8

import flask
import auth
import model
import util
import config
import wtforms
from flask.ext import wtf
from main import app

class ArtistUpdateForm(wtf.Form):

  name = wtforms.StringField('Name', filters=[util.strip_filter])
  artist_type = wtforms.StringField('Type', filters=[util.strip_filter])
  gender = wtforms.SelectField('Gender', choices=[(t, t.title()) for t in model.Artist.gender._choices],default="none")
  mbid = wtforms.StringField('mbid', filters=[util.strip_filter])
  website = wtforms.StringField('website', filters=[util.strip_filter])
  image_url = wtforms.StringField('image_url', filters=[util.strip_filter])

###############################################################################
# Artists List
###############################################################################
@app.route('/artist/')
@auth.login_required
def artist_list():
  artist_dbs, artist_cursor = model.Artist.get_dbs(
      # user_key=auth.current_user_key(),
    )

  return flask.render_template(
      'artist/artist_list.html',
      html_class='artist-list',
      title='Artist List',
      artist_dbs=artist_dbs,
      next_url=util.generate_next_url(artist_cursor),
    )
###############################################################################
# Artists Create
###############################################################################  
@app.route('/artist/create/', methods=['GET', 'POST'])
@auth.login_required
def artist_create():
  form = ArtistUpdateForm()
  if form.validate_on_submit():
    artist_db = model.Artist()

    form.populate_obj(artist_db)
    artist_db.put()
    return flask.redirect('/artist/%i' % artist_db.key.id())
  return flask.render_template(
      '/artist/artist_update.html',
      html_class='artist-create',
      title='Create Artist',
      form=form,
    )
###############################################################################
# Artists View
###############################################################################
@app.route('/artist/<int:artist_id>/')
@auth.login_required
def artist_view(artist_id):
  artist_db = model.Artist.get_by_id(artist_id)
  # if not artist_db or artist_db.user_key != auth.current_user_key():
  #   flask.abort(404)
  return flask.render_template(
      'artist/artist_view.html',
      html_class='artist-view',
      title=artist_db.name,
      artist_db=artist_db,
    )

###############################################################################
# Artists Update
###############################################################################
@app.route('/artist/<int:artist_id>/update/', methods=['GET', 'POST'])
@auth.login_required
def artist_update(artist_id):
  artist_db = model.Artist.get_by_id(artist_id)
  # if not artist_db or artist_db.user_key != auth.current_user_key():
  #   flask.abort(404)
  form = ArtistUpdateForm(obj=artist_db)
  if form.validate_on_submit():
    form.populate_obj(artist_db)
    artist_db.put()
    return flask.redirect(flask.url_for('artist_list', order='-modified'))
  return flask.render_template(
      'artist/artist_update.html',
      html_class='artist-update',
      title=artist_db.name,
      form=form,
      artist_db=artist_db,
    )