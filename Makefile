migrate:
	python manage.py migrate

run:
	open http://127.0.0.1:8000/ && python manage.py runserver

superuser:
	python manage.py createsuperuser