COMPOSE = docker compose

up:
	${COMPOSE} up -d --remove-orphans
down:
	${COMPOSE} down

restart: down up

server:
	uvicorn src.main:app --reload