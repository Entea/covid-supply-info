init:
	cp backend/.env.dev backend/.env

helpmegod:
	docker-compose up

thanksgod:
	docker-compose down