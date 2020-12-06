.PHONY: build up start down destroy stop restart logs prepare_db

build:
	docker-compose -f docker-compose.yml build $(c)
up:
	docker-compose -f docker-compose.yml up -d $(c)
start:
	docker-compose -f docker-compose.yml start $(c)
down:
	docker-compose -f docker-compose.yml down $(c)
destroy:
	docker-compose -f docker-compose.yml down -v $(c)
stop:
	docker-compose -f docker-compose.yml stop $(c)
restart:
	docker-compose -f docker-compose.yml stop $(c)
	docker-compose -f docker-compose.yml up -d $(c)
logs:
	docker-compose -f docker-compose.yml logs --tail=100 -f $(c)

first_start: up
	docker-compose -f docker-compose.yml exec web ./manage.py collectstatic
	docker-compose -f docker-compose.yml exec web ./manage.py migrate
	docker-compose -f docker-compose.yml exec web ./manage.py createsuperuser
