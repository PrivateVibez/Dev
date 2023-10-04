#!/bin/sh
python manage.py migrate
# Execute the command as root


# If you really need to switch back to a different user for subsequent commands, 
# then you would have to handle that user switching in the Dockerfile itself 
# (like using USER directive in Dockerfile) or use gosu or similar tools.

# Continue with the rest of your script
exec "$@"
