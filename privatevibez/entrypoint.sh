#!/bin/sh

# Path to a sentinel file which indicates that the initial setup was done
SENTINEL_FILE="/privatevibez/.initial_setup_done"

# Check if the sentinel file exists
if [ ! -f "$SENTINEL_FILE" ]; then
    # Run initialization commands
    python manage.py migrate || exit 1
    python manage.py cities --import=country,region,city || exit 1
    python manage.py loaddata accounts/fixtures/staffdata.json || exit 1

    # Create the sentinel file to mark the initial setup as done
    touch $SENTINEL_FILE
fi

# If you need to switch back to a different user for subsequent commands, 
# handle that user switching in the Dockerfile itself 
# (like using the USER directive in Dockerfile) or use gosu or similar tools.

# Continue with the rest of your script
exec "$@"
