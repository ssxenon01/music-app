__author__ = 'xenon'
import flask
from main import app

@app.route('/moods')
def mood():
    template = 'mood.html'
    if flask.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        template = 'mood_content.html'
    return flask.render_template(template,
                                 html_class='mood'
                                 )
