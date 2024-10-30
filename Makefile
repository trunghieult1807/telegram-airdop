CONTAINER=bot

.PHONY: build
build:
	docker compose build

.PHONY: up
up:
	docker compose up --remove-orphans

.PHONY: down
down:
	docker compose down

.PHONY: destroy
destroy:
	docker compose down --volumes --rmi all

.PHONY: shell
shell:
	docker compose run $(CONTAINER) sh

.PHONY: log
log:
	docker compose logs -f $(CONTAINER)

.PHONY: safe
safe:
	@if [ -z "$(app)" ]; then \
		echo "Error: Please choose correct app."; \
		exit 1; \
	fi
	@mv api_data/$(app)/api_data.new.json api_data/$(app)/api_data.json
