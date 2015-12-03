#!/bin/bash
# pwd is the git repo.
set -e

# For XVFB Selenium tests.
echo "Starting Browser for Smoke Tests"
export DISPLAY=:99.0

echo 'Starting a server'
./manage.py shell < ./scripts/create_user_and_superuser.py
./manage.py generatedata
./manage.py runsslserver &
sleep 3

echo 'Running Smoke tests'
source venv_smoketests/bin/activate
export VARIABLE_PATH=$('pwd')/scripts/travis/variables.json

cd smoketests
xvfb-run --server-args="-screen 0, 1280x1024x16" py.test --driver=firefox --baseurl=https://localhost:8000 --destructive --variables=$VARIABLE_PATH .
echo 'Booyahkasha!'
