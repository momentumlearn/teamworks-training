.PHONY: dev test

dev:
	FLASK_APP=api.app:create_app FLASK_ENV=development flask run

test:
	pytest
