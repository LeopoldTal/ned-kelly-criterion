import json
from ..services.auth_service import get_current_user
from ..services.variant_service import get_variant_for_user, record_variant_success, record_variant_failure
from .formatters import format_collection, format_variant

def get_variant(event, context):
	user = get_current_user(event)
	if user is None:
		return { 'statusCode': 401 }
	
	# FIXME: how do I get the variant id from the route?
	variant = get_variant_for_user(1, user.user_id)
	if variant is None:
		return { 'statusCode': 404 }
	
	return {
			'statusCode': 200,
			'body': json.dumps(format_variant(variant))
		}

def post_variant_success(event, context):
	# TODO
	pass

def post_variant_failure(event, context):
	# TODO
	pass

# TODO: delete variant
