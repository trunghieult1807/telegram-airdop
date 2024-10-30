CONTAINER=bot

.PHONY: build
build:
	docker build -t telegram-airdop-bot .

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

.PHONE: env
env:
	export $(cat .env | xargs)

.PHONY: deploy
EC2_USER=ec2-user
EC2_IP=3.26.190.206
KEY_PATH=../mrluas.pem
deploy:
	@docker save -o telegram-airdop-bot.tar telegram-airdop-bot:latest \
	&& scp -i $(KEY_PATH) telegram-airdop-bot.tar $(EC2_USER)@$(EC2_IP):~/images/telegram-airdop-bot.tar \
	&& scp -i $(KEY_PATH) compose.yaml $(EC2_USER)@$(EC2_IP):~/images/compose.yaml \
	&& ssh -i $(KEY_PATH) $(EC2_USER)@$(EC2_IP) 'docker stop telegram-airdop-bot || true && docker rm telegram-airdop-bot || true && docker load -i ~/images/telegram-airdop-bot.tar && cd images && docker-compose up -d'