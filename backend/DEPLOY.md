### How to deploy

Copy .env.dev to .env file, then edit:
```
SECRET_KEY=put something weird here
DJANGO_SETTINGS_MODULE=backend.production
STATIC_ROOT = '/var/www/covid-supply/static'
```

Run commands:
```
# copy static files
python manage.py collectstatic
# run migrations
python manage.py migrate
# restart gunicorn
systemctl restart gunicorn
```

Gunicorn systemd file, note the `!SET_PORT_HERE!` thingie:
```
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
Type=simple
# the specific user that our service will run as
User=www-data
Group=www-data
# another option for an even more restricted service is
# DynamicUser=yes
# see http://0pointer.net/blog/dynamic-users-with-systemd.html
WorkingDirectory=/opt/covid-supply/backend
ExecStart=/opt/covid-supply/backend/venv/bin/gunicorn -b 127.0.0.1:!SET_PORT_HERE! -w 3 backend.wsgi
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

Create log dir & file:
```
mkdir -p /var/log/django
touch /var/log/django/error.log
chown -R www-data /var/log/django
```
