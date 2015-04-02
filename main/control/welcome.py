# coding: utf-8
import logging
import flask
from google.appengine.api import memcache
import config
import model
import socket
import struct
from main import app
from google.appengine.ext import ndb
import api.sons
# ##############################################################################
# Welcome
# ##############################################################################
network = api.sons.SonsNetwork()
network.enable_caching()
@app.route('/sons')
def sons():
    """
        Sons Stream
        ffmpeg -i "http://stream.sons.mn:6055/COHC/amlst:2915e5da-f54f-4c82-adde-9f49b43c5fed/playlist.m3u8" -f mp3 -acodec mp3 -ab 128k -ar 44100 -vn aнэг.mp3
    """
    result = network.search_for_track('Бороо,Татар').get_next_page()
    for track in result:
        if track.artist_id is not None:
            artist = network.get_artist(track.artist_id)
    return ''


@app.route('/')
def welcome():
    template = 'welcome.html'
    if flask.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        template = 'welcome_content.html'

    discover_list = get_discover_list()
    new_songs = get_new_songs()
    return flask.render_template(template,
                                 html_class='welcome',
                                 discover_list=discover_list,
                                 new_songs=new_songs
                                 )


def get_new_songs():
    data = memcache.get('get_new_songs')
    if data is not None:
        return data
    else:
        data = model.Track.query().order(model.Track.created).fetch(limit=8)
        memcache.set('get_new_songs', data, 60*60)
        return data


def get_discover_list():
    data = memcache.get('get_discover_list')
    if data is not None:
        return data
    else:
        data = model.Track.query(model.Track.stream_url != '' and model.Track.modified != None).order(-model.Track.modified).fetch(limit=10)
        memcache.set('get_discover_list', data, 60*60)
        return data


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


# ##############################################################################
# Checking if accessing from Mongolia
# ##############################################################################


# @app.before_request
def limit_remote_addr():
    # TODO: allow SEO bot

    if flask.request.remote_addr not in ['127.0.0.1', '0.1.0.3']:
        if not address_in_network(flask.request.remote_addr):
            flask.abort(403)  # Forbidden


# ##############################################################################
# List of Mongolian IP Subnet
# ##############################################################################


def address_in_network(ip):
    net_list = [
        '14.0.59.0/24',
        '27.123.212.0/22',
        '43.228.128.0/22',
        '43.231.112.0/22',
        '43.242.240.0/22',
        '43.243.160.0/22',
        '43.250.124.0/22',
        '46.36.196.81/32',
        '46.36.196.82/31',
        '46.36.196.84/30',
        '46.36.196.88/31',
        '46.36.196.90/32',
        '49.0.128.0/17',
        '49.156.1.0/24',
        '103.8.60.0/24',
        '103.9.88.0/22',
        '103.10.20.0/22',
        '103.11.192.0/22',
        '103.14.36.0/22',
        '103.17.108.0/23',
        '103.20.152.0/22',
        '103.23.48.0/22',
        '103.26.192.0/22',
        '103.29.144.0/22',
        '103.29.199.0/24',
        '103.48.116.0/24',
        '103.50.204.0/22',
        '103.51.60.0/24',
        '103.229.120.0/22',
        '103.229.176.0/22',
        '103.230.82.0/24',
        '103.242.44.0/22',
        '103.254.120.0/22',
        '104.128.128.0/24',
        '104.167.203.0/24',
        '112.72.0.0/20',
        '115.187.88.0/22',
        '119.40.96.0/21',
        '121.101.176.0/21',
        '122.201.16.0/20',
        '122.254.64.0/18',
        '124.158.64.0/18',
        '150.129.140.0/22',
        '180.149.64.0/18',
        '180.235.160.0/19',
        '182.160.0.0/18',
        '183.81.168.0/22',
        '183.177.96.0/20',
        '202.5.192.0/20',
        '202.9.40.0/21',
        '202.21.96.0/19',
        '202.55.176.0/20',
        '202.61.97.0/24',
        '202.70.32.0/20',
        '202.72.240.0/21',
        '202.126.88.0/21',
        '202.131.0.0/21',
        '202.131.224.0/19',
        '202.170.64.0/19',
        '202.179.0.0/19',
        '202.180.216.0/21',
        '203.34.37.0/24',
        '203.91.112.0/21',
        '203.160.48.0/21',
        '203.169.48.0/21',
        '203.174.26.0/24',
        '203.194.112.0/21',
        '204.231.134.0/23',
        '218.100.84.0/24',
    ]

    for net in net_list:
        ipaddr = struct.unpack('L', socket.inet_aton(ip))[0]
        netaddr, bits = net.split('/')
        netmask = struct.unpack('L', socket.inet_aton(netaddr))[0] & ((2L << int(bits) - 1) - 1)
        if ipaddr & netmask == netmask:
            return True
    return False
