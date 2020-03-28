init:
	cp backend/.env.dev backend/.env

helpmegod:
	docker-compose up --build

thanksgod:
	docker-compose down
