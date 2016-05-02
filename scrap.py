# encoding: utf-8

import sys, os
import requests
from lxml import html
import unicodedata

from sqlalchemy import Column, String, Integer, create_engine, func
from sqlalchemy.types import DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLAlchemy session and db opening
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
engine = create_engine('sqlite:///{}'.format(os.path.join(SCRIPT_DIR, 'data.db')))

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


# Declares object structure included in database
class Quotes(Base):
    __tablename__ = 'quotes_fr'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    category = Column(String)
    author = Column(String)
    last_check = Column(DateTime(timezone=True), default=func.now())
    sqlite_autoincrement = True


def scrape_french():
    url = 'http://www.abc-citations.com/themes/'

    page = requests.get(url)
    html_tree = html.fromstring(page.text)

    them_list = html_tree.xpath('//*[@id="list-themes"]/li/a/span[1]')
    nb_list = html_tree.xpath('//*[@id="list-themes"]/li/a/span[2]')

    for i, them in enumerate(them_list):
        nb_page = int(nb_list[i].text)/16 + 1
        for n in range(nb_page):
            catg = unicodedata.normalize('NFKD', unicode(them.text.encode('ascii', 'ignore')))
            url_parse = '{0}{1}/page/{2}/'.format(url, catg.lower(), n+1)

            target = requests.get(url_parse)
            local_tree = html.fromstring(target.text)
            quote_list = local_tree.xpath('//*[@id="content"]/section[2]/div/div/div[1]/div/article/div[1]/p[1]/text()')
            author_list = local_tree.xpath('//*[@id="content"]/section[2]/div/div/div[1]/div/article/div[1]/p[2]/text()')
            for j, quote in enumerate(quote_list):
                # print '{0}:\t{1} ({2})'.format(author_list[j].encode('utf-8').strip(),
                #                                quote.encode('utf-8').strip(), them.text.encode('utf-8'))

                get_or_create(session=session, model=Quotes, category=them.text,
                              author=author_list[j].strip(), text=quote.strip())


def get_or_create(session, model, **kwargs):
    quote = session.query(model).filter_by(**kwargs).first()
    if quote:
        return quote
    else:
        quote = model(**kwargs)
        session.add(quote)
        session.commit()
        return quote


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    quote = session.query()