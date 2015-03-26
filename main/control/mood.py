__author__ = 'xenon'
import logging
import flask
from google.appengine.api import memcache
import config
import model
import socket
import struct
from main import app

@app.route('/moods')
def mood():
    return flask.render_template('mood.html',
                                 html_class='mood'
                                 )
