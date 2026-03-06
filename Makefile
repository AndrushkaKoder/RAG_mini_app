COMPOSE = docker compose

up:
	${COMPOSE} up -d
down:
	${COMPOSE} down

restart: down up