# coding: utf-8
import logging
import flask
from google.appengine.api import memcache
import config
import model
import socket
import struct

from main import app


# ##############################################################################
# Welcome
# ##############################################################################
@app.before_request
def limit_remote_addr():
    if flask.request.remote_addr not in ['127.0.0.1', '0.1.0.3']:
        if address_in_network(flask.request.remote_addr):
            # logging.info(flask.request.remote_addr)
            flask.abort(403)  # Forbidden


@app.route('/')
def welcome():
    discover_list = get_discover_list()
    new_songs = get_new_songs()
    logging.info(flask.request.remote_addr)
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


def address_in_network(ip):
    net_list = [
        '14.0.59.0',
        '27.123.212.0',
        '43.228.128.0',
        '43.231.112.0',
        '43.242.240.0',
        '43.243.160.0',
        '43.250.124.0',
        '46.36.196.81',
        '46.36.196.82',
        '46.36.196.84',
        '46.36.196.88',
        '46.36.196.90',
        '49.0.128.0',
        '49.156.1.0',
        '103.8.60.0',
        '103.9.88.0',
        '103.10.20.0',
        '103.11.192.0',
        '103.14.36.0',
        '103.17.108.0',
        '103.20.152.0',
        '103.23.48.0',
        '103.26.192.0',
        '103.29.144.0',
        '103.29.199.0',
        '103.48.116.0',
        '103.50.204.0',
        '103.51.60.0',
        '103.229.120.0',
        '103.229.176.0',
        '103.230.82.0',
        '103.242.44.0',
        '103.254.120.0',
        '104.128.128.0',
        '104.167.203.0',
        '112.72.0.0',
        '115.187.88.0',
        '119.40.96.0',
        '121.101.176.0',
        '122.201.16.0',
        '122.254.64.0',
        '124.158.64.0',
        '150.129.140.0',
        '180.149.64.0',
        '180.235.160.0',
        '182.160.0.0',
        '183.81.168.0',
        '183.177.96.0',
        '202.5.192.0',
        '202.9.40.0',
        '202.21.96.0',
        '202.55.176.0',
        '202.61.97.0',
        '202.70.32.0',
        '202.72.240.0',
        '202.126.88.0',
        '202.131.0.0',
        '202.131.224.0',
        '202.170.64.0',
        '202.179.0.0',
        '202.180.216.0',
        '203.34.37.0',
        '203.91.112.0',
        '203.160.48.0',
        '203.169.48.0',
        '203.174.26.0',
        '203.194.112.0',
        '204.231.134.0',
        '218.100.84.0',
    ]
    for net in net_list:
        ipaddr = struct.unpack('L', socket.inet_aton(ip))[0]
        netaddr, bits = net.split('/')
        netmask = struct.unpack('L', socket.inet_aton(netaddr))[0] & ((2L << int(bits) - 1) - 1)
        if ipaddr & netmask == netmask:
            return True
    return False
