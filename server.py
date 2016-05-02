# encoding: utf-8

import os
import random
import flask

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Quotes, Base

# SQLAlchemy session and db opening
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
engine = create_engine('sqlite:///{}'.format(os.path.join(SCRIPT_DIR, 'data.db')))

Session = sessionmaker(bind=engine)
session = Session()

app = flask.Flask(__name__)


def get_quote(theme=None):
    if theme:
        q_list = session.query(Quotes).filter_by(category=theme).all()
    else:
        q_list = session.query(Quotes).all()
    qid = random.randrange(1, len(q_list))
    return q_list[qid]


@app.route('/api/random', methods=['GET'])
def quote_random():
    quote = get_quote()
    return flask.jsonify({'Auteur': quote.author, 'Citation': quote.text})


@app.route('/api/quote', methods=['POST'])
def quote_theme():
    theme = flask.request.json.get('theme', None)
    quote = get_quote(theme)
    return flask.jsonify({'Auteur': quote.author, 'Citation': quote.text})


@app.route('/api/themes', methods=['GET'])
def get_themes():
    themes = set()
    for citation in session.query(Quotes).all():
        themes.add(citation.category)
    return flask.jsonify({'Themes': list(themes)})


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    app.run(host='0.0.0.0', port=8008, debug=True)
