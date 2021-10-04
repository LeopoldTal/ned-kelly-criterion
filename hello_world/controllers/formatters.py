from ..orm import Experiment, Variant

def format_collection(l, collection_name : str, format_item = lambda x: x):
	return {
		'total': len(l),
		collection_name: [ format_item(item) for item in l ]
	}

def format_experiment(experiment: Experiment):
	return {
		'experiment_id': experiment.experiment_id,
		'name': experiment.name,
		'creation_date': experiment.creation_date.isoformat(),
		'update_date': experiment.update_date.isoformat(),
		'variants': [ format_variant(variant) for variant in experiment.variants ]
	}

def format_variant(variant: Variant):
	return {
		'variant_id': variant.variant_id,
		'name': variant.name,
		'nb_successes': variant.nb_successes,
		'nb_failures': variant.nb_failures,
		'experiment_id': variant.experiment_id,
		'creation_date': variant.creation_date.isoformat(),
		'update_date': variant.update_date.isoformat(),
	}
