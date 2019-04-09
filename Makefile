.PHONY: migrate

migrate:
	alembic -c alembic.dev.ini upgrade head

gen-mock-data:
	docker-compose exec plugin python gen_mock_data.py
