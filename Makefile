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

EC2_USER=ec2-user
EC2_IP=13.236.160.192
KEY_PATH=../mrluas.pem
.PHONY: deploy
deploy:
	@docker save -o aio2.tar aio2:latest \
	&& scp -i $(KEY_PATH) aio2.tar $(EC2_USER)@$(EC2_IP):~/images/aio2.tar \
	&& ssh -i $(KEY_PATH) $(EC2_USER)@$(EC2_IP) 'docker stop aio2 || true && docker rm aio2 || true && docker load -i ~/images/aio2.tar && docker run -v /home/ec2-user/sessions:/app/sessions -d --name aio2 aio2:latest'

