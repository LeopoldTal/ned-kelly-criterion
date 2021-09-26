from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class Experiment(Base):
	__tablename__ = 'experiments'
	
	experiment_id = Column(Integer, primary_key = True)
	name = Column(String, nullable = False)
	user_id = Column(Integer, ForeignKey('users.user_id'), nullable = False, index = True)
	creation_date = Column(DateTime, nullable = False)
	update_date = Column(DateTime, nullable = False)
	deletion_date = Column(DateTime, nullable = True)
	
	user = relationship('User', back_populates = 'experiments')
	variants = relationship('Variant', back_populates = 'experiment')
	
	def __repr__(self) -> str:
		return f'''Experiment(
	experiment_id = {self.experiment_id!r},
	name = {self.name!r},
	user_id = {self.user_id!r},
	creation_date = {self.creation_date!r},
	update_date = {self.update_date!r},
	deletion_date = {self.deletion_date!r}
)'''
