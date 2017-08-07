#!/bin/bash
# pwd is the git repo.
set -e

# Installing dependencies for UI tests
if [[ $TEST_SUITE == "ui" ]]; then
  sudo pip install tox
  echo "Downloading and extracting geckodriver"
  wget https://github.com/mozilla/geckodriver/releases/download/v0.18.0/geckodriver-v0.18.0-linux64.tar.gz
  mkdir $HOME/geckodriver && tar -xzf geckodriver-v0.18.0-linux64.tar.gz -C $HOME/geckodriver
fi

if [[ $TEST_SUITE == "lint" ]]; then
    sudo pip install -r requirements/dev.txt
fi

if [[ $TEST_SUITE == "docker" ]]; then
  sudo pip install docker-compose
fi
