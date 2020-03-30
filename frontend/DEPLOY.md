Regular update:
```
yarn
yarn build
systemctl restart tirek-next
```

Systemd file
```
[Unit]
Description=Nextjs frontend for tirek.kg
After=network.target

[Service]
Environment=NODE_ENV=production
Type=simple
User=nodejs
ExecStart=/usr/bin/node /opt/covid-supply/frontend/node_modules/.bin/next start --hostname=127.0.0.1 --port=3000
WorkingDirectory=/opt/covid-supply/frontend
Restart=on-failure

[Install]
WantedBy=multi-user.target
```