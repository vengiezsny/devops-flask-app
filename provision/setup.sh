mkdir -p provision
cat > provision/setup.sh <<'SH'
#!/usr/bin/env bash
set -e

apt-get update
DEBIAN_FRONTEND=noninteractive apt-get -y upgrade

apt-get install -y python3 python3-venv python3-pip git rsync

APP_USER=flaskapp
id -u $APP_USER >/dev/null 2>&1 || useradd -m -s /bin/bash $APP_USER

REPO_DIR="/home/${APP_USER}/app"
if [ -d /vagrant ] && [ -n "$(ls -A /vagrant)" ]; then
  mkdir -p "$REPO_DIR"
  rsync -a --exclude='.git' /vagrant/ "$REPO_DIR/"
  chown -R $APP_USER:$APP_USER "$REPO_DIR"
else
  GIT_REPO_URL="REPLACE_WITH_YOUR_REPO_URL"
  if [ "$GIT_REPO_URL" != "REPLACE_WITH_YOUR_REPO_URL" ]; then
    git clone "$GIT_REPO_URL" "$REPO_DIR"
    chown -R $APP_USER:$APP_USER "$REPO_DIR"
  else
    echo "No source in /vagrant and no GIT_REPO_URL set. Exiting."
    exit 1
  fi
fi

sudo -u $APP_USER bash -c "
cd $REPO_DIR
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
if [ -f requirements.txt ]; then
  pip install -r requirements.txt
fi
"

SERVICE_FILE=/etc/systemd/system/flaskapp.service
cat > $SERVICE_FILE <<'EOF'
[Unit]
Description=Flask App Service
After=network.target

[Service]
User=flaskapp
Group=flaskapp
WorkingDirectory=/home/flaskapp/app
Environment="PATH=/home/flaskapp/app/venv/bin"
ExecStart=/home/flaskapp/app/venv/bin/python -u -m flask run --host=0.0.0.0 --port=5000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

cat > /home/flaskapp/app/.flaskenv <<'EOF'
FLASK_APP=app.py
FLASK_ENV=production
EOF
chown -R flaskapp:flaskapp /home/flaskapp/app

systemctl daemon-reload
systemctl enable flaskapp.service
systemctl start flaskapp.service

# Show status
systemctl status flaskapp.service --no-pager || true
SH

# make executable
chmod +x provision/setup.sh
