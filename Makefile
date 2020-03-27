init:
	cp backend/.env.dev backend/.env

helpmegod:
	docker-compose up > /dev/null &

thanksgod:
	docker-compose down