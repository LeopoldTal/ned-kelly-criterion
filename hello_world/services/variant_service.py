from ..orm import Variant
from ..db import get_variant_by_id

def get_variant_for_user(variant_id : int, user_id : int) -> Variant:
	variant = get_variant_by_id(variant_id)
	if variant is None:
		return None
	if variant.experiment.user_id != user_id:
		return None
	return variant

def record_variant_success(variant_id : int, user_id : int) -> None:
	# TODO
	pass

def record_variant_failure(variant_id : int, user_id : int) -> None:
	# TODO
	pass
