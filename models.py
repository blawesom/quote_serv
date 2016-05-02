# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Integer, func
from sqlalchemy.types import DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Quotes(Base):
    __tablename__ = 'quotes_fr'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    category = Column(String)
    author = Column(String)
    last_check = Column(DateTime(timezone=True), default=func.now())
    sqlite_autoincrement = True
