generate:
	alembic revision --m="$(name)" --autogenerate

migrate:
	alembic upgrade head


run_celery_worker:
	celery -A src.tasks.celery_app:celery_instance worker -l INFO --pool=solo


run_celery_beat:
	celery -A src.tasks.celery_app:celery_instance beat -l INFO