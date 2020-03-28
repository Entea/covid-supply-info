

### Backend Environment

```
sudo apt-get install libpq-dev python3-dev
sudo apt-get install binutils libproj-dev gdal-bin 
```

Run `cp .env.dev .env` and make sure it contains what you need :)

```
docker-compose up -d #make sure that db works :)
```

```
1. git clone git@github.com:Entea/covid-supply-info.git ~/projects/covid-supply-info
2. cd ~/projects/covid-supply-info/backend
3. python3 -m venv venv
4. source venv/bin/activate
5. pip install -r requirements.txt
6. python manage.py runserver
```

#### How to run migrations?
```
python manage.py migrate
```
or
```
docker compose exec make migrate
```

#### How to create an admin?
```
python manage.py createsuperuser
```
or
```
docker-compose exec make createsuperuser
```

#### How to update dependencies?
```
pip freeze > requirements.txt
```
