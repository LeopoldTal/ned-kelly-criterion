from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
	__tablename__ = 'users'
	
	user_id = Column(Integer, primary_key = True)
	email_address = Column(String(320), nullable = True, unique = True)
	api_key_id = Column(String(128), nullable = True, index = True, unique = True)
	creation_date = Column(DateTime, nullable = False)
	update_date = Column(DateTime, nullable = False)
	deletion_date = Column(DateTime, nullable = True)
	
	experiments = relationship('Experiment', back_populates = 'user')
	
	def __repr__(self) -> str:
		return f'''User(
	user_id = {self.user_id!r},
	email_address = {self.email_address!r},
	api_key_id = {self.api_key_id!r},
	creation_date = {self.creation_date!r},
	update_date = {self.update_date!r},
	deletion_date = {self.deletion_date!r}
)'''
