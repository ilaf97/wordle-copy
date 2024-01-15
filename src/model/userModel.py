from src import db
from sqlalchemy import *


class User(db.Model):
	id = Column(Integer, primary_key=True)
	username = Column(String(20), nullable=False)
	email = Column(String(80), nullable=False)
	join_date = Column(DateTime(timezone=False),
						   server_default=func.now())

