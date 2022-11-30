from sqlalchemy import func
from src.model import db
from sqlalchemy import *


class Guess(db.Model):
	user_id = Column(Integer, primary_key=True)
	guess_date = Column(DateTime(timezone=False),
						   server_default=func.now(),
						   primary_key=True)
	guess_str = Column(String(30), nullable=False)
