# coding: utf-8

import logging

import flask

from api import helpers
import config

from main import app


@app.errorhandler(400)  # Bad Request
@app.errorhandler(401)  # Unauthorized
@app.errorhandler(404)  # Not Found
@app.errorhandler(405)  # Method Not Allowed
@app.errorhandler(410)  # Gone
@app.errorhandler(418)  # I'm a Teapot
@app.errorhandler(500)  # Internal Server Error
def error_handler(e):
    logging.exception(e)
    try:
        e.code
    except AttributeError:
        e.code = 500
        e.name = u'Сервэрт алдаа гарлаа'

    if flask.request.path.startswith('/api/'):
        return helpers.handle_error(e)

    return flask.render_template(
        'error.html',
        title=u'Алдаа %d (%s)!!1' % (e.code, e.name),
        html_class='error-page',
        error=e,
    ), e.code


@app.errorhandler(403)  # Forbidden
def error_403(e):
    return flask.render_template(
        '403.html',
        html_class='403',
        ip=flask.request.remote_addr
    )


if config.PRODUCTION:
    @app.errorhandler(Exception)
    def production_error_handler(e):
        return error_handler(e)
