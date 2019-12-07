.PHONY: dev

dev:
	FLASK_APP=api FLASK_ENV=development flask run
