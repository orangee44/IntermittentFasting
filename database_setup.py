import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Restaurant(Base):
	__tablename__ = 'restaurant'
	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)


	# Added this serialize function to be able to send JSON objects in serializable format
	@property
	def serialize(self):
		return {
		'name': self.name,
		'id': self.id,
		}

class FastingStatus(Base):
	__tablename__ = 'fasting_status'
	fasting = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)
	restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
	restaurant = relationship(Restaurant)

	# Added this serialize function to be able to send JSON objects in serializable format
	@property
	def serialize(self):
		return {
		'fasting': self.fasting,
		'id': self.id,
		}

class Observations(Base):
	__tablename__ = 'observ'
	description = Column(String(250), nullable = False)
	id = Column(Integer, primary_key = True)
	restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
	restaurant = relationship(Restaurant)

	# Added this serialize function to be able to send JSON objects in serializable format
	@property
	def serialize(self):
		return {
		'fasting': self.fasting,
		'id': self.id,
		}


class MenuItem(Base):
	__tablename__ = 'menu_item'
	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)
	course = Column(String(250))
	description = Column(String(250))
	calories = Column(String(8))
	restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
	restaurant = relationship(Restaurant)
	
	# We added this serialize function to be able to send JSON objects in a
	# serializable format
	@property
	def serialize(self):
		return {
			'name': self.name,
			'description': self.description,
			'id': self.id,
			'calories': self.calories,
			'course': self.course,
		}

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)


