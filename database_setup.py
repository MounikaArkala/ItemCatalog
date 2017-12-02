import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    category_name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, cascade="save-update, merge, delete")


class Item(Base):
    __tablename__ = 'item'

    item_name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(2500))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category, cascade="save-update, merge, delete")
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, cascade="save-update, merge, delete")


# serialize function to be able to send JSON objects in a
# serializable format
    @property
    def serialize(self):

        return {
            'item_name': self.item_name,
            'description': self.description,
            'id': self.id,
        }


engine = create_engine('sqlite:///categoryitemlist.db')


Base.metadata.create_all(engine)
