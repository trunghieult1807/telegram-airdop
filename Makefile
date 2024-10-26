CONTAINER=bot

.PHONY: build
build:
	docker compose build

.PHONY: up
up:
	docker compose up

.PHONY: down
down:
	docker compose down

.PHONY: destroy
destroy:
	docker compose down --volumes --rmi all

.PHONY: shell
shell:
	docker compose exec $(CONTAINER) sh

.PHONY: log
log:
	docker compose logs -f $(CONTAINER)
