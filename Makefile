EC2_USER=ec2-user
EC2_IP=3.26.190.206
KEY_PATH=mrluas.pem
CONTAINER=bot
DEVCONTAINER=bot-dev

.PHONY: build
build:
	docker build -t telegram-airdop-bot .

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

.PHONE: env
env:
	export $(cat .env | xargs)

.PHONY: deploy
EC2_USER=ec2-user
EC2_IP=3.25.135.123
KEY_PATH=../mrluas.pem
deploy:
	@docker save -o telegram-airdop-bot.tar telegram-airdop-bot:latest \
	&& scp -i $(KEY_PATH) telegram-airdop-bot.tar $(EC2_USER)@$(EC2_IP):~/images/telegram-airdop-bot.tar \
	&& scp -i $(KEY_PATH) compose.yaml $(EC2_USER)@$(EC2_IP):~/images/compose.yaml \
	&& ssh -i $(KEY_PATH) $(EC2_USER)@$(EC2_IP) 'docker stop telegram-airdop-bot || true && docker rm telegram-airdop-bot || true && docker load -i ~/images/telegram-airdop-bot.tar && cd images && docker-compose up -d'

.PHONY: ssh
ssh:
	ssh -i $(KEY_PATH) $(EC2_USER)@$(EC2_IP)

# Local run
.PHONY: build-dev
build-dev:
	docker compose -f docker/compose.dev.yaml build

.PHONY: run-dev
run-dev:
	docker compose -f docker/compose.dev.yaml exec $(DEVCONTAINER) python3 main.py

.PHONY: start-dev
start-dev:
	docker compose -f docker/compose.dev.yaml up -d

.PHONY: shell-dev
shell-dev:
	docker compose -f docker/compose.dev.yaml exec $(DEVCONTAINER) sh

.PHONY: stop-dev
stop-dev:
	docker compose -f docker/compose.dev.yaml down

.PHONY: destroy-dev
destroy-dev:
	docker compose -f docker/compose.dev.yaml down --volumes --rmi all
