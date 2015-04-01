import flask
import model
from main import app
__author__ = 'Gundsambuu'



@app.route('/genres')
def genres():
    template = 'genres.html'
    if flask.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        template = 'genre_content.html'


    genre_list = model.Track.genre_list()
    return flask.render_template(template,
                                 html_class='genres',
                                 genre_list=genre_list,
                                 active=flask.request.args.get('type', ''))

