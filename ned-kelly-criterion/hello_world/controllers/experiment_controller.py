import json
from ..services.auth_service import get_current_user
from ..services.experiment_service import create_experiment_with_variants, get_experiment_for_user
from .formatters import format_collection, format_experiment, format_variant

def get_experiments(event, context):
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
