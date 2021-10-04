import json
from ..services.auth_service import get_current_user
from ..services.experiment_service import create_experiment_with_variants, create_variant, get_experiment_for_user
from .formatters import format_collection, format_experiment, format_variant

def get_experiment_suggest_variant(event, context):
	user = get_current_user(event)
	if user is None:
		return { 'statusCode': 401 }
	
	# FIXME: how do I get the experiment id from the route?
	experiment = get_experiment_for_user(1, user.user_id)
	if experiment is None:
		return { 'statusCode': 404 }
	
	if len(experiment.variants) == 0:
		return {
			'statusCode': 400,
			'body': json.dumps({ 'message': 'Experiment has no variants' })
		}
	
	# TODO: multi-armed bandit
	chosen_variant = experiment.variants[0]
	return {
		'statusCode': 200,
		'body': json.dumps({
			'id': chosen_variant.id,
			'name': chosen_variant.name
		})
	}

def get_experiments(event, context):
	# TODO: Plug this in to a route
	user = get_current_user(event)
	if user is None:
		return { 'statusCode': 401 }
	
	return {
			'statusCode': 200,
			'body': json.dumps(
				format_collection(user.experiments, 'experiments', format_experiment)
			)
		}

def get_experiment(event, context):
	user = get_current_user(event)
	if user is None:
		return { 'statusCode': 401 }
	
	# FIXME: how do I get the experiment id from the route?
	experiment = get_experiment_for_user(1, user.user_id)
	if experiment is None:
		return { 'statusCode': 404 }
	
	return {
			'statusCode': 200,
			'body': json.dumps(format_experiment(experiment))
		}

def get_experiment_variants(event, context):
	user = get_current_user(event)
	if user is None:
		return { 'statusCode': 401 }
	
	# FIXME: how do I get the experiment id from the route?
	experiment = get_experiment_for_user(13, user.user_id)
	if experiment is None:
		return { 'statusCode': 404 }
	
	return {
			'statusCode': 200,
			'body': json.dumps(
				format_collection(experiment.variants, 'variants', format_variant)
			)
		}

def post_experiment(event, context):
	user = get_current_user(event)
	if user is None:
		return { 'statusCode': 401 }
	
	# FIXME: how do I get postdata?
	# create_experiment_with_variants(name = ?, user_id = user.user_id, variant_names = ?)

def post_experiment_variant(event, context):
	user = get_current_user(event)
	if user is None:
		return { 'statusCode': 401 }
	
	# FIXME: how do I get the experiment id from the route?
	experiment = get_experiment_for_user(13, user.user_id)
	if experiment is None:
		return { 'statusCode': 404 }
	
	# FIXME: how do I get postdata?
	# create_variant(name = ?)
