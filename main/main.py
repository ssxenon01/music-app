# coding: utf-8

import flask

import config
import util
import sys
reload(sys) 
sys.setdefaultencoding('utf8')
app = flask.Flask(__name__)
app.config.from_object(config)
app.jinja_env.line_statement_prefix = '#'
app.jinja_env.line_comment_prefix = '##'
app.jinja_env.globals.update(
    check_form_fields=util.check_form_fields,
    is_iterable=util.is_iterable,
    slugify=util.slugify,
    update_query_argument=util.update_query_argument,
  )

import auth
import control
import model
import task
import control.track
import control.artist

from api import helpers
api = helpers.Api(app)

import api.v1


if config.DEVELOPMENT:
  from werkzeug import debug
  app.wsgi_app = debug.DebuggedApplication(app.wsgi_app, evalex=True)
  app.testing = False
