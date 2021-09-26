from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class Variant(Base):
	__tablename__ = 'variants'
	
	variant_id = Column(Integer, primary_key = True)
	name = Column(String, nullable = False)
	experiment_id = Column(Integer, ForeignKey('experiments.experiment_id'), nullable = False, index = True)
	nb_successes = Column(Integer, nullable = False)
	nb_failures = Column(Integer, nullable = False)
	creation_date = Column(DateTime, nullable = False)
	update_date = Column(DateTime, nullable = False)
	deletion_date = Column(DateTime, nullable = True)
	
	experiment = relationship('Experiment', back_populates = 'variants')
	
	def __repr__(self) -> str:
		return f'''Variant(
	variant_id = {self.variant_id!r},
	name = {self.name!r},
	experiment_id = {self.experiment_id!r},
	nb_successes = {self.nb_successes!r},
	nb_failures = {self.nb_failures!r},
	creation_date = {self.creation_date!r},
	update_date = {self.update_date!r},
	deletion_date = {self.deletion_date!r}
)'''
	
	@property
	def nb_trials(self):
		return self.nb_successes + self.nb_failures
