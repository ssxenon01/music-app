music-app
========

**music-app** is the Music Platform based on gae-init , Google
App Engine using Flask, Bootstrap and tons of other cool features.

The latest version is always accessible from
[http://listen-fm.appspot.com](http://listen-fm.appspot.com)

Running the Development Environment
-----------------------------------

    $ cd /path/to/music-app
    $ ./run.py -s

To test it visit `http://localhost:8080/` in your browser.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

To watch for changes of your `*.less` & `*.coffee` files and compile them
automatically to `*.css` & `*.js` execute in another bash:

    $ ./run.py -w

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

For a complete list of commands:

    $ ./run.py -h

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

Gulp is used only for watching for changes and live reloading the page.
Install [Gulp][] as a global package:

    $ npm install -g gulp

and then from the root execute with no arguments:

    $ gulp

Deploying on Google App Engine
------------------------------

Before deploying make sure that the `app.yaml` and `config.py` are up to date
and you ran the `run.py` script to minify all the static files:

    $ ./run.py -m
    $ appcfg.py update main

Tech Stack
----------

  - [Google App Engine][], [NDB][]
  - [Jinja2][], [Flask][], [Flask-RESTful][], [Flask-WTF][]
  - [CoffeeScript][], [Less][]
  - [Bootstrap][], [Font Awesome][], [Social Buttons][]
  - [jQuery][], [NProgress][], [Moment.js][]
  - [OpenID][] sign in (Google, Facebook, Twitter)
  - [Python 2.7][], [pip][], [virtualenv][]
  - [Gulp][], [Bower][]

Requirements
------------

  - [Google App Engine SDK for Python][]
  - [Node.js][], [pip][], [virtualenv][]
  - [OSX][] or [Linux][] or [Windows][]

Author
------

[![Xenon on stackoverflow.com][xenonflair]][xenon]

[bootstrap]: http://getbootstrap.com/
[bower]: http://bower.io/
[coffeescript]: http://coffeescript.org/
[flask-restful]: https://flask-restful.readthedocs.org
[flask-wtf]: https://flask-wtf.readthedocs.org
[flask]: http://flask.pocoo.org/
[font awesome]: http://fortawesome.github.com/Font-Awesome/
[google app engine sdk for python]: https://developers.google.com/appengine/downloads
[google app engine]: https://developers.google.com/appengine/
[gulp]: http://gulpjs.com
[jinja2]: http://jinja.pocoo.org/docs/
[jquery]: http://jquery.com/
[less]: http://lesscss.org/
[lesscss]: http://lesscss.org/
[linux]: http://www.ubuntu.com
[xenon]: http://stackoverflow.com/users/1176640/xenon
[xenonflair]: http://stackexchange.com/users/flair/1207323.png
[moment.js]: http://momentjs.com/
[ndb]: https://developers.google.com/appengine/docs/python/ndb/
[node.js]: http://nodejs.org/
[nprogress]: http://ricostacruz.com/nprogress/
[openid]: http://en.wikipedia.org/wiki/OpenID
[osx]: http://www.apple.com/osx/
[pip]: http://www.pip-installer.org/
[python 2.7]: https://developers.google.com/appengine/docs/python/python27/using27
[social buttons]: http://lipis.github.io/bootstrap-social/
[virtualenv]: http://www.virtualenv.org/
[windows]: http://windows.microsoft.com/
