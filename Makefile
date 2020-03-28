init:
	cp backend/.env.dev backend/.env

helpmegod:
	docker-compose up -d

thanksgod:
	docker-compose down
