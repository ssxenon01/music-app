# coding: utf-8

from __future__ import absolute_import

from google.appengine.api import users
import flask

import auth
import model
import util

from main import app


@app.route('/signin/google/')
def signin_google():
    auth.save_request_params()
    google_url = users.create_login_url(flask.url_for('google_authorized'))
    return flask.redirect(google_url)


@app.route('/_s/callback/google/authorized/')
def google_authorized():
    google_user = users.get_current_user()
    if google_user is None:
        flask.flash('You denied the request to sign in.')
        return flask.redirect(util.get_next_url())

    user_db = retrieve_user_from_google(google_user)
    return auth.signin_user_db(user_db)


def retrieve_user_from_google(google_user):
    auth_id = 'federated_%s' % google_user.user_id()
    user_db = model.User.get_by('auth_ids', auth_id)
    if user_db:
        if not user_db.admin and users.is_current_user_admin():
            user_db.admin = True
            user_db.put()
        return user_db

    return auth.create_user_db(
        auth_id=auth_id,
        name=util.create_name_from_email(google_user.email()),
        username=google_user.email(),
        email=google_user.email(),
        verified=True,
        admin=users.is_current_user_admin(),
    )
