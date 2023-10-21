#!/bin/sh
SENTINEL_FILE="/privatevibez/.initial_setup_done"
if [ ! -f "$SENTINEL_FILE" ]; then
    python manage.py migrate || exit 1
    python manage.py cities --import=country,region,city || exit 1
    python manage.py loaddata accounts/fixtures/staffdata.json || exit 1
    touch $SENTINEL_FILE
fi
exec "$@"