COMPOSE = docker compose

up:
	${COMPOSE} up -d
down:
	${COMPOSE} down

restart: down up

server:
	uvicorn src.main:app --reload