#!/bin/bash

# if [ ! -d "/app/migrations" ]; then
#     flask db init
# fi

# flask db migrate -m "Initial migration"

# # Run migrations
# flask db upgrade

# Start the Flask application
# flask run --host=0.0.0.0

exec "$@"