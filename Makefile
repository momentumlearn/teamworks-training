.PHONY: dev test

dev:
	FLASK_APP=api FLASK_ENV=development flask run

test:
	pytest
