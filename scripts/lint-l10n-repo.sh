#!/bin/bash

# Run this from the project root--not from this directory!

set -x

POSTATUS_FILE=kitsune/sumo/static/postatus.txt

if [[ -d locale ]]; then
    git -C locale fetch
    git -C locale checkout origin/master
else
    git clone https://github.com/mozilla-l10n/sumo-l10n.git locale
fi

GIT_COMMIT=$(git -C locale rev-parse HEAD)

echo -e "l10n git hash: ${GIT_COMMIT}\n" > $POSTATUS_FILE
make lint-l10n >> $POSTATUS_FILE

if [[ "$?" -eq 0 && "$1" == "--push" ]]; then
    git -C locale remote add mozilla-it https://github.com/mozilla-it/sumo-l10n-prod.git
    git -C locale push -f mozilla-it HEAD:master
fi
