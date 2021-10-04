from ..orm import Experiment
from ..db import create_experiment, create_variant, get_experiment_by_id

def get_experiment_for_user(experiment_id : int, user_id : int) -> Experiment:
	experiment = get_experiment_by_id(experiment_id)
	if experiment is None:
		return None
	if experiment.user_id != user_id:
		return None
	return experiment

def create_experiment_with_variants(name : str, user_id : int, variant_names : list[str]) -> Experiment:
	experiment = create_experiment(name = name, user_id = user_id)
	print('Created experiment with id', experiment.experiment_id, 'for user', user_id)
	for variant_name in variant_names:
		variant = create_variant(name = variant_name, experiment_id = experiment.experiment_id)
		print('Created variant with id', variant.variant_id,
			'in experiment', experiment.experiment_id, 'for user', user_id)
	return experiment
