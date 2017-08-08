#!/bin/bash
# pwd is the git repo.
set -ex

echo "Starting XVFB for UI tests"
export DISPLAY=:99.0


echo 'Starting a server'
sh -e /etc/init.d/xvfb start
docker-compose exec web ./manage.py migrate
docker-compose exec web ./manage.py create_travis_user_and_superuser
docker-compose exec web ./manage.py generatedata
# Reindex elasticsearch
docker-compose exec web ./manage.py esreindex --delete
GECKO_DRIVER_PATH = $HOME/geckodriver/geckodriver
export PYTEST_BASE_URL="http://localhost:8000"
export PYTEST_ADDOPTS="--verbose --driver=Firefox --variables=scripts/travis/variables.json --driver-path=GECKO_DRIVER_PATH"

echo 'Running UI tests'
tox

echo 'Booyahkasha!'
