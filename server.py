# encoding: utf-8

import os
import flask

from sqlalchemy import Column, String, Integer, create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from  sqlalchemy.types import DateTime, String, Integer
import random

# SQLAlchemy session and db opening
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
engine = create_engine('sqlite:///{}'.format(os.path.join(SCRIPT_DIR, 'data.db')))

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

app = flask.Flask(__name__)


# Declares object structure included in database
class Quotes(Base):
    __tablename__ = 'quotes_fr'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    category = Column(String)
    author = Column(String)
    last_check = Column(DateTime(timezone=True), default=func.now())
    sqlite_autoincrement = True


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
