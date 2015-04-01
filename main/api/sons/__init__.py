from google.appengine.api import memcache

__author__ = 'Gundsambuu'

from StringIO import StringIO
import gzip
import logging
import hashlib
import json
import time
import sys
from httplib import HTTPConnection
import htmlentitydefs
from urllib import quote_plus as url_quote_plus

import six

STATUS_INVALID_SERVICE = 2
STATUS_INVALID_METHOD = 3
STATUS_AUTH_FAILED = 4
STATUS_INVALID_FORMAT = 5
STATUS_INVALID_PARAMS = 6
STATUS_INVALID_RESOURCE = 7
STATUS_TOKEN_ERROR = 8
STATUS_INVALID_SK = 9
STATUS_INVALID_API_KEY = 10
STATUS_OFFLINE = 11
STATUS_SUBSCRIBERS_ONLY = 12
STATUS_INVALID_SIGNATURE = 13
STATUS_TOKEN_UNAUTHORIZED = 14
STATUS_TOKEN_EXPIRED = 15

EVENT_ATTENDING = '0'
EVENT_MAYBE_ATTENDING = '1'
EVENT_NOT_ATTENDING = '2'

PERIOD_OVERALL = 'overall'
PERIOD_7DAYS = "7day"
PERIOD_3MONTHS = '3month'
PERIOD_6MONTHS = '6month'
PERIOD_12MONTHS = '12month'

DOMAIN_ENGLISH = 0
DOMAIN_GERMAN = 1
DOMAIN_SPANISH = 2
DOMAIN_FRENCH = 3
DOMAIN_ITALIAN = 4
DOMAIN_POLISH = 5
DOMAIN_PORTUGUESE = 6
DOMAIN_SWEDISH = 7
DOMAIN_TURKISH = 8
DOMAIN_RUSSIAN = 9
DOMAIN_JAPANESE = 10
DOMAIN_CHINESE = 11

COVER_SMALL = 0
COVER_MEDIUM = 1
COVER_LARGE = 2
COVER_EXTRA_LARGE = 3
COVER_MEGA = 4

IMAGES_ORDER_POPULARITY = "popularity"
IMAGES_ORDER_DATE = "dateadded"

USER_MALE = 'Male'
USER_FEMALE = 'Female'


class _Network(object):
    """
    A music social network website such as sons.mn or
    one with a sons.mn-compatible API.
    """

    def __init__(
            self, name, homepage, ws_server, session_key, urls):
        """
            name: the name of the network
            homepage: the homepage URL
            ws_server: the URL of the webservices server
            api_key: a provided API_KEY
            api_secret: a provided API_SECRET
            session_key: a generated session_key or None
            password_hash: the output of pylast.md5(password) where password is
                the user's password
            domain_names: a dict mapping each DOMAIN_* value to a string domain
                name
            urls: a dict mapping types to URLs

            You should use a preconfigured network object through a
            get_*_network(...) method instead of creating an object
            of this class, unless you know what you're doing.
        """

        self.name = name
        self.homepage = homepage
        self.ws_server = ws_server
        self.session_key = session_key
        self.urls = urls

        self.cache_backend = None
        self.proxy_enabled = False
        self.proxy = None
        self.last_call_time = 0
        self.limit_rate = False

    """def __repr__(self):
        attributes = ("name", "homepage", "ws_server", "api_key", "api_secret",
            "session_key", "submission_server", "password_hash",
            "domain_names", "urls")

        text = "pylast._Network(%s)"
        args = []
        for attr in attributes:
            args.append("=".join((attr, repr(getattr(self, attr)))))

        return text % ", ".join(args)
    """

    def __str__(self):
        return "%s Network" % self.name

    def get_artist(self, artist_id):
        """
            Return an Artist object
        """

        response = _Request(network=self, method_name='artists/fetchById?id=' + artist_id, params={},
                            request_method='GET').execute(True)
        artist = response['artist']

        return Artist(id=artist['id'], image=artist['image'], name=artist['name'], num_albums=artist['numAlbums'],
                      num_tracks=artist['numTracks'])

    def get_track(self, track_id):
        """
            Return an Artist object
        """

        response = _Request(self, 'tracks/fetchById?id=' + track_id, params={}, request_method='GET').execute(True)
        track = response['track']
        return Track(id=track['id'], image=track['image'], title=track['title'], album_name=track['albumName'],
                     length=track['length'], media_path=track['mediaPath'], origin=track['origin'],
                     youtube=track['youtube'], lyrics=track['lyrics'], artist_id=track['artistId'],
                     artist_name=track['artistName'])

    def get_track_list(self, page_number=1):
        response = _Request(self, 'tracks/fetchByPage?page=' + str(page_number), params={},
                            request_method='GET').execute(True)
        tracks = response['tracks']
        seq = []
        for track in tracks:
            seq.append(Track(id=track['id'], image=track['image'], title=track['title'], album_name=track['albumName'],
                             length=track['length'], media_path=track['mediaPath'], origin=track['origin'],
                             youtube=track['youtube'], lyrics=track['lyrics'], artist_id=track['artistId'],
                             artist_name=track['artistName']))

        return seq

    def get_album(self, album_id):
        """
            Return an Album object
        """
        response = _Request(self, 'track/fetchById?id=' + album_id, params={}, request_method='GET').execute(True)
        album = response['album']
        return Album(id=album['id'], title=album['title'], image=album['image'], artist_name=album['artist_name'],
                     artist_id=album['artist_id'], year=album['year'], duration=album['duration'],
                     num_tracks=album['num_tracks'])

    def _get_url(self, domain, url_type):
        return "http://%s/%s" % (
            self._get_language_domain(domain), self.urls[url_type])

    def _delay_call(self):
        """
            Makes sure that web service calls are at least 0.2 seconds apart.
        """

        # Delay time in seconds from section 4.4 of http://www.sons.mn/api/tos
        DELAY_TIME = 0.2
        now = time.time()

        time_since_last = now - self.last_call_time

        if time_since_last < DELAY_TIME:
            time.sleep(DELAY_TIME - time_since_last)

        self.last_call_time = now

    def enable_proxy(self, host, port):
        """Enable a default web proxy"""

        self.proxy = [host, _number(port)]
        self.proxy_enabled = True

    def disable_proxy(self):
        """Disable using the web proxy"""

        self.proxy_enabled = False

    def is_proxy_enabled(self):
        """Returns True if a web proxy is enabled."""

        return self.proxy_enabled

    def _get_proxy(self):
        """Returns proxy details."""

        return self.proxy

    def enable_rate_limit(self):
        """Enables rate limiting for this network"""
        self.limit_rate = True

    def disable_rate_limit(self):
        """Disables rate limiting for this network"""
        self.limit_rate = False

    def is_rate_limited(self):
        """Return True if web service calls are rate limited"""
        return self.limit_rate

    def enable_caching(self):
        """Enables caching request-wide for all cacheable calls.

        * file_path: A file path for the backend storage file. If
        None set, a temp file would probably be created, according the backend.
        """

        self.cache_backend = _ShelfCacheBackend()

    def disable_caching(self):
        """Disables all caching features."""

        self.cache_backend = None

    def is_caching_enabled(self):
        """Returns True if caching is enabled."""

        return not (self.cache_backend is None)

    def _get_cache_backend(self):

        return self.cache_backend

    def search_for_album(self, album_name):
        """Searches for an album by its name. Returns a AlbumSearch object.
        Use get_next_page() to retrieve sequences of results."""

        return AlbumSearch(album_name, self)

    def search_for_artist(self, artist_name):
        """Searches of an artist by its name. Returns a ArtistSearch object.
        Use get_next_page() to retrieve sequences of results."""

        return ArtistSearch(artist_name, self)

    def search_for_track(self, query):
        """Searches of a track by its name and its artist. Set artist to an
        empty string if not available.
        Returns a TrackSearch object.
        Use get_next_page() to retrieve sequences of results."""

        return TrackSearch(query, self)

    def get_track_by_sons_id(self, sons_id):
        """Looks up a track by its MusicBrainz ID"""

        params = {"id": sons_id}

        doc = _Request(self, "track.getInfo", params).execute(True)

        return Track(_extract(doc, "name", 1), _extract(doc, "name"), self)

    def get_artist_by_sonsid(self, sons_id):
        """Loooks up an artist by its MusicBrainz ID"""

        params = {"id": sons_id}

        doc = _Request(self, "artist.getInfo", params).execute(True)

        return Artist(_extract(doc, "name"), self)

    def get_album_by_sonsid(self, sons_id):
        """Looks up an album by its MusicBrainz ID"""

        params = {"id": sons_id}

        doc = _Request(self, "album.getInfo", params).execute(True)

        return Album(_extract(doc, "artist"), _extract(doc, "name"), self)


    def get_play_links(self, link_type, things, cacheable=True):
        method = link_type + ".getPlaylinks"
        params = {}

        for i, thing in enumerate(things):
            if link_type == "artist":
                params['artist[' + str(i) + ']'] = thing
            elif link_type == "album":
                params['artist[' + str(i) + ']'] = thing.artist
                params['album[' + str(i) + ']'] = thing.title
            elif link_type == "track":
                params['artist[' + str(i) + ']'] = thing.artist
                params['track[' + str(i) + ']'] = thing.title

        doc = _Request(self, method, params).execute(cacheable)

        seq = []

        for node in doc.getElementsByTagName("externalids"):
            spotify = _extract(node, "spotify")
            seq.append(spotify)

        return seq

    def get_artist_play_links(self, artists, cacheable=True):
        return self.get_play_links("artist", artists, cacheable)

    def get_album_play_links(self, albums, cacheable=True):
        return self.get_play_links("album", albums, cacheable)

    def get_track_play_links(self, tracks, cacheable=True):
        return self.get_play_links("track", tracks, cacheable)


class SonsNetwork(_Network):
    """A sons.mn network object

    api_key: a provided API_KEY
    api_secret: a provided API_SECRET
    session_key: a generated session_key or None
    password_hash: the output of pylast.md5(password) where password is the
        user's password

    Most read-only webservices only require an api_key and an api_secret, see
    about obtaining them from:
    http://www.sons.mn/api/account
    """

    def __init__(self, session_key="", ):
        _Network.__init__(
            self,
            name="sons.mn",
            homepage="http://sons.fm",
            ws_server=("sons.mn", "/api/"),
            session_key=session_key,
            urls={
                "album": "music/%(artist)s/%(album)s",
                "artist": "music/%(artist)s",
                "track": "music/%(artist)s/_/%(title)s",
                "search": "search/tracks/%(query)s"
            }
        )

    def __repr__(self):
        return "pylast.LastFMNetwork(%s)" % (", ".join(
            ("'%s'" % self.session_key)))


class _ShelfCacheBackend(object):
    """Used as a backend for caching cacheable requests."""

    def get_xml(self, key):
        return memcache.get('sons_tmp_' + key)

    def set_xml(self, key, json_string):
        memcache.set('sons_tmp_' + key, json_string, 60)


class _Request(object):
    """Representing an abstract web service operation."""

    def __init__(self, network, method_name, params={}, request_method='POST'):

        self.network = network
        self.params = {}

        for key in params:
            self.params[key] = _unicode(params[key])

        self.method_name = method_name
        self.request_method = request_method
        if network.is_caching_enabled():
            self.cache = network._get_cache_backend()


    def _get_cache_key(self):
        """
        The cache key is a string of concatenated sorted names and values.
        """

        keys = list(self.params.keys())
        keys.sort()

        cache_key = str()

        for key in keys:
            if key != "api_sig" and key != "api_key" and key != "sk":
                cache_key += key + self.params[key]

        cache_key += self.method_name

        return hashlib.sha1(cache_key.encode("utf-8")).hexdigest()

    def _get_cached_response(self):
        """Returns a file object of the cached response."""

        ca = self.cache.get_xml(self._get_cache_key())
        if ca is None:
            response = self._download_response()
            self.cache.set_xml(self._get_cache_key(), response)

        return self.cache.get_xml(self._get_cache_key())

    def _download_response(self):
        """Returns a response body string from the server."""

        if self.network.limit_rate:
            self.network._delay_call()

        data = []
        for name in self.params.keys():
            data.append('='.join((
                name, url_quote_plus(_string(self.params[name])))))
        data = '&'.join(data)

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': "keep-alive",
            'X-CSRF-Guard': 'on'
        }
        (HOST_NAME, HOST_SUBDIR) = self.network.ws_server
        logging.info(self.network.ws_server)
        if self.network.is_proxy_enabled():
            conn = HTTPConnection(
                host=self.network._get_proxy()[0],
                port=self.network._get_proxy()[1])

            try:
                conn.request(
                    method=self.request_method, url="http://" + HOST_NAME + HOST_SUBDIR + self.method_name,
                    body=data, headers=headers)
            except Exception as e:
                raise NetworkError(self.network, e)

        else:
            conn = HTTPConnection(host=HOST_NAME)

            try:
                conn.request(
                    method=self.request_method, url=HOST_SUBDIR + self.method_name, body=data, headers=headers)
            except Exception as e:
                raise NetworkError(self.network, e)

        try:
            buf = StringIO(conn.getresponse().read())
            f = gzip.GzipFile(fileobj=buf)
            response_text = _unicode(f.read())
        except Exception as e:
            raise MalformedResponseError(self.network, e)
        response_text = response_text.replace(")]}',", '')
        self._check_response_for_errors(response_text)
        return response_text

    def execute(self, cacheable=False):
        """Returns the XML DOM response of the POST Request from the server"""

        if self.network.is_caching_enabled() and cacheable:
            response = self._get_cached_response()
        else:
            response = self._download_response()

        return json.loads(_string(response))

    def _check_response_for_errors(self, response):
        """Checks the response for errors and raises one if any exists."""

        try:
            doc = json.loads(_string(response))
        except Exception as e:
            logging.error(response)
            raise MalformedResponseError(self.network, e)

        if not doc['success']:
            e = doc['error']
            status = doc['code']
            details = doc
            raise WSError(self.network, status, details)


def _string_output(funct):
    def r(*args):
        return _string(funct(*args))

    return r


def _pad_list(given_list, desired_length, padding=None):
    """
        Pads a list to be of the desired_length.
    """

    while len(given_list) < desired_length:
        given_list.append(padding)

    return given_list


class _BaseObject(object):
    """An abstract webservices object."""

    network = None

    def __init__(self, network, ws_prefix):
        self.network = network
        self.ws_prefix = ws_prefix

    def _request(self, method_name, cacheable=True, params=None):
        if not params:
            params = self._get_params()
        return _Request(self.network, method_name, params).execute(cacheable)

    def _get_params(self):
        """Returns the most common set of parameters between all objects."""

        return {}

    def __hash__(self):
        # Convert any ints (or whatever) into strings
        values = map(six.text_type, self._get_params().values())

        return hash(self.network) + hash(six.text_type(type(self)) + "".join(
            list(self._get_params().keys()) + list(values)
        ).lower())

    def _extract_cdata_from_request(self, method_name, tag_name, params):
        doc = self._request(method_name, True, params)

        return doc.getElementsByTagName(
            tag_name)[0].firstChild.wholeText.strip()


class WSError(Exception):
    """Exception related to the Network web service"""

    def __init__(self, network, status, details):
        self.status = status
        self.details = details
        self.network = network

    @_string_output
    def __str__(self):
        return self.details

    def get_id(self):
        """Returns the exception ID, from one of the following:
            STATUS_INVALID_SERVICE = 2
            STATUS_INVALID_METHOD = 3
            STATUS_AUTH_FAILED = 4
            STATUS_INVALID_FORMAT = 5
            STATUS_INVALID_PARAMS = 6
            STATUS_INVALID_RESOURCE = 7
            STATUS_TOKEN_ERROR = 8
            STATUS_INVALID_SK = 9
            STATUS_INVALID_API_KEY = 10
            STATUS_OFFLINE = 11
            STATUS_SUBSCRIBERS_ONLY = 12
            STATUS_TOKEN_UNAUTHORIZED = 14
            STATUS_TOKEN_EXPIRED = 15
        """

        return self.status


class MalformedResponseError(Exception):
    """Exception conveying a malformed response from sons.mn."""

    def __init__(self, network, underlying_error):
        self.network = network
        self.underlying_error = underlying_error

    def __str__(self):
        return "Malformed response from sons.mn. Underlying error: %s" % str(
            self.underlying_error)


class NetworkError(Exception):
    """Exception conveying a problem in sending a request to sons.mn"""

    def __init__(self, network, underlying_error):
        self.network = network
        self.underlying_error = underlying_error

    def __str__(self):
        return "NetworkError: %s" % str(self.underlying_error)


class _Opus(_BaseObject):
    """An album or track."""

    artist = None
    title = None

    __hash__ = _BaseObject.__hash__

    def __init__(self, artist, title, network, ws_prefix):
        """
        Create an opus instance.
        # Parameters:
            * artist: An artist name or an Artist object.
            * title: The album or track title.
            * ws_prefix: 'album' or 'track'
        """

        _BaseObject.__init__(self, network, ws_prefix)

        if isinstance(artist, Artist):
            self.artist = artist
        else:
            self.artist = Artist(artist, self.network)

        self.title = title

    def __repr__(self):
        return "pylast.%s(%s, %s, %s)" % (
            self.ws_prefix.title(), repr(self.artist.name),
            repr(self.title), repr(self.network))

    @_string_output
    def __str__(self):
        return _unicode("%s - %s") % (
            self.get_artist().get_name(), self.get_title())

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        a = self.get_title().lower()
        b = other.get_title().lower()
        c = self.get_artist().get_name().lower()
        d = other.get_artist().get_name().lower()
        return (a == b) and (c == d)

    def __ne__(self, other):
        return not self.__eq__(other)

    def _get_params(self):
        return {
            'artist': self.get_artist().get_name(),
            self.ws_prefix: self.get_title()}

    def get_artist(self):
        """Returns the associated Artist object."""

        return self.artist

    def get_title(self, properly_capitalized=False):
        """Returns the artist or track title."""
        if properly_capitalized:
            self.title = _extract(
                self._request(self.ws_prefix + ".getInfo", True), "name")

        return self.title

    def get_name(self, properly_capitalized=False):
        """Returns the album or track title (alias to get_title())."""

        return self.get_title(properly_capitalized)

    def get_id(self):
        """Returns the ID on the network."""

        return _extract(
            self._request(self.ws_prefix + ".getInfo", cacheable=True), "id")

    def get_playcount(self):
        """Returns the number of plays on the network"""

        return _number(_extract(
            self._request(
                self.ws_prefix + ".getInfo", cacheable=True), "playcount"))


    def get_sons_id(self):
        """Returns the MusicBrainz ID of the album or track."""

        return _extract(
            self._request(self.ws_prefix + ".getInfo", cacheable=True), "sons_id")


class Album(object):
    """An album."""

    def __init__(self, id, title, image, artist_name, artist_id, year, duration, num_tracks):
        self.id = id
        self.title = title
        self.image = image
        self.artist_name = artist_name
        self.artist_id = artist_id
        self.year = year
        self.duration = duration
        self.num_tracks = num_tracks


class Artist():
    """An artist."""

    def __init__(self, id, image, name, num_albums, num_tracks):
        self.id = id
        self.image = image
        self.name = name
        self.num_albums = num_albums
        self.num_tracks = num_tracks


class Track():
    """A sons.mn track."""

    def __init__(self, id, image, title,
                 album_name, length, media_path, origin, youtube, lyrics, artist_id,artist_name):
        self.id = id
        self.image = image
        self.title = title
        self.album_name = album_name
        self.length = length
        self.media_path = media_path
        self.origin = origin
        self.youtube = youtube
        self.lyrics = lyrics
        self.artist_id = artist_id
        self.artist_name = artist_name


class _Search(_BaseObject):
    """An abstract class. Use one of its derivatives."""

    def __init__(self, ws_prefix, search_terms, network):
        _BaseObject.__init__(self, network, ws_prefix)

        self._ws_prefix = ws_prefix
        self.search_terms = search_terms

        self._last_page_index = 0

    def _get_params(self):
        params = {}

        for key in self.search_terms.keys():
            params[key] = self.search_terms[key]

        return params

    def get_total_result_count(self):
        """Returns the total count of all the results."""
        self.search_terms['page'] = 1
        doc = self._request(self._ws_prefix, True)

        return _extract(doc, "totalNumResults")

    def _retrieve_page(self, page_index):
        """Returns the node of matches to be processed"""

        params = self._get_params()
        params["page"] = page_index
        return self._request(self._ws_prefix, True, params)


    def _retrieve_next_page(self):
        self._last_page_index += 1
        return self._retrieve_page(self._last_page_index)


class AlbumSearch(_Search):
    """Search for an album by name."""

    def __init__(self, album_name, network):
        _Search.__init__(self, "album", {"album": album_name}, network)

    def get_next_page(self):
        """Returns the next page of results as a sequence of Album objects."""

        master_node = self._retrieve_next_page()

        seq = []
        for node in master_node.getElementsByTagName("album"):
            seq.append(Album(
                _extract(node, "artist"),
                _extract(node, "name"),
                self.network))

        return seq


class ArtistSearch(_Search):
    """Search for an artist by artist name."""

    def __init__(self, artist_name, network):
        _Search.__init__(self, "artist", {"artist": artist_name}, network)

    def get_next_page(self):
        """Returns the next page of results as a sequence of Artist objects."""

        master_node = self._retrieve_next_page()

        seq = []
        for node in master_node.getElementsByTagName("artist"):
            artist = Artist(_extract(node, "name"), self.network)
            artist.listener_count = _number(_extract(node, "listeners"))
            seq.append(artist)

        return seq


class TrackSearch(_Search):
    """
    Search for a track by track title. If you don't want to narrow the results
    down by specifying the artist name, set it to empty string.
    """

    def __init__(self, query, network):
        _Search.__init__(
            self,
            "search/tracks",
            {"keywords": query},
            network)

    def get_next_page(self):
        """Returns the next page of results as a sequence of Track objects."""
        seq = []
        page = self._retrieve_next_page()
        for track in page['results']:
            seq.append(Track(id=track['id'], image=track['image'], title=track['title'], album_name=track['albumName'],
                             length=track['length'], media_path=track['mediaPath'], origin=track['origin'],
                             youtube=track['youtube'], lyrics=track['lyrics'], artist_id=track['artistId'],
                             artist_name=track['artistName']))
        return seq


def md5(text):
    """Returns the md5 hash of a string."""

    h = hashlib.md5()
    h.update(_unicode(text).encode("utf-8"))

    return h.hexdigest()


def _unicode(text):
    if isinstance(text, six.binary_type):
        return six.text_type(text, "utf-8")
    elif isinstance(text, six.text_type):
        return text
    else:
        return six.text_type(text)


def _string(string):
    """For Python2 routines that can only process str type."""
    if isinstance(string, str):
        return string
    casted = six.text_type(string)
    if sys.version_info[0] == 2:
        casted = casted.encode("utf-8")
    return casted


def _extract(node, name, index=0):
    """Extracts a value from the xml string"""

    return node[name]


def _extract_element_tree(node, index=0):
    """Extract an element tree into a multi-level dictionary

    NB: If any elements have text nodes as well as nested
    elements this will ignore the text nodes"""

    def _recurse_build_tree(rootNode, targetDict):
        """Recursively build a multi-level dict"""

        def _has_child_elements(rootNode):
            """Check if an element has any nested (child) elements"""

            for node in rootNode.childNodes:
                if node.nodeType == node.ELEMENT_NODE:
                    return True
            return False

        for node in rootNode.childNodes:
            if node.nodeType == node.ELEMENT_NODE:
                if _has_child_elements(node):
                    targetDict[node.tagName] = {}
                    _recurse_build_tree(node, targetDict[node.tagName])
                else:
                    val = None if node.firstChild is None else \
                        _unescape_htmlentity(node.firstChild.data.strip())
                    targetDict[node.tagName] = val
        return targetDict

    return _recurse_build_tree(node, {})


def _extract_all(node, name, limit_count=None):
    """Extracts all the values from the xml string. returning a list."""

    seq = []

    for i in range(0, len(node.getElementsByTagName(name))):
        if len(seq) == limit_count:
            break

        seq.append(_extract(node, name, i))

    return seq


def _url_safe(text):
    """Does all kinds of tricks on a text to make it safe to use in a url."""

    return url_quote_plus(url_quote_plus(_string(text))).lower()


def _number(string):
    """
        Extracts an int from a string.
        Returns a 0 if None or an empty string was passed.
    """

    if not string:
        return 0
    elif string == "":
        return 0
    else:
        try:
            return int(string)
        except ValueError:
            return float(string)


def _unescape_htmlentity(string):
    # string = _unicode(string)

    mapping = htmlentitydefs.name2codepoint
    for key in mapping:
        string = string.replace("&%s;" % key, unichr(mapping[key]))

    return string


def extract_items(topitems_or_libraryitems):
    """
    Extracts a sequence of items from a sequence of TopItem or
    LibraryItem objects.
    """

    seq = []
    for i in topitems_or_libraryitems:
        seq.append(i.item)

    return seq


class ScrobblingError(Exception):
    def __init__(self, message):
        Exception.__init__(self)
        self.message = message

    @_string_output
    def __str__(self):
        return self.message


class BannedClientError(ScrobblingError):
    def __init__(self):
        ScrobblingError.__init__(
            self, "This version of the client has been banned")


class BadAuthenticationError(ScrobblingError):
    def __init__(self):
        ScrobblingError.__init__(self, "Bad authentication token")


class BadTimeError(ScrobblingError):
    def __init__(self):
        ScrobblingError.__init__(
            self, "Time provided is not close enough to current time")


class BadSessionError(ScrobblingError):
    def __init__(self):
        ScrobblingError.__init__(
            self, "Bad session id, consider re-handshaking")


# End of file
