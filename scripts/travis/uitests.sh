#!/bin/bash
# pwd is the git repo.
set -ex

echo "Starting XVFB for UI tests"
#export DISPLAY=:99.0
#/sbin/start-stop-daemon --start --quiet --pidfile /tmp/custom_xvfb_99.pid --make-pidfile --background --exec /usr/bin/Xvfb -- :99 -ac -screen 0 1280x1024x16

echo 'Starting a server'
docker-compose exec web ./manage.py migrate
docker-compose exec web ./manage.py create_travis_user_and_superuser
docker-compose exec web ./manage.py generatedata
# Reindex elasticsearch
docker-compose exec web ./manage.py esreindex --delete

GECKO_DRIVER_PATH="$HOME/geckodriver/geckodriver"
PYTEST_ADDOPTS="--verbose --driver=Firefox --base-url=http://localhost:8000"
PYTEST_ADDOPTS="${PYTEST_ADDOPTS} --variables=scripts/travis/variables.json --driver-path=${GECKO_DRIVER_PATH}"

echo 'Running UI tests'
tox

echo 'Booyahkasha!'
