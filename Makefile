.PHONY: api test

api:
	FLASK_APP=api.app:create_app FLASK_ENV=development flask run

test:
	pytest
