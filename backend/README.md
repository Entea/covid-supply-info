

### Backend Environment

```
sudo apt-get install libpq-dev python3-dev
sudo apt-get install binutils libproj-dev gdal-bin 
```

```
docker-compose up -d #make sure that db works :)
```

```
1. git clone git@github.com:Entea/covid-supply-info.git ~/projects/covid-supply-info
2. cd ~/projects/covid-supply-info/backend
3. python3 -m venv venv
4. source venv/bin/activate
5. pip install -r requirements.txt
6. DISTRIBUTOR_DB_NAME=distributor DISTRIBUTOR_DB_USER=master DISTRIBUTOR_DB_PASSWORD=123456 DISTRIBUTOR_DB_PORT=5435 python manage.py runserver
```

#### How to create an admin?
```
DISTRIBUTOR_DB_NAME=distributor DISTRIBUTOR_DB_USER=master DISTRIBUTOR_DB_PASSWORD=123456 DISTRIBUTOR_DB_PORT=5435 python manage.py createsuperuser
```

#### How to update dependencies?
```
pip freeze > requirements.txt
```