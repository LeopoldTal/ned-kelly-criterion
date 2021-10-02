from sqlalchemy.orm.exc import NoResultFound
from ..orm import User
from ..db import get_user_by_api_key_id

def get_current_user(event) -> User:
	api_key_id = event['requestContext']['identity']['apiKeyId']
	if api_key_id is None:
		return None
	try:
		user = get_user_by_api_key_id(api_key_id)
	except NoResultFound:
		return None
	print(f'Authenticated user {user.user_id} <{user.email_address}> ({user.api_key_id})')
	return user
