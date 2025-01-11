#!/bin/bash

# Start the backend service
cd /app/backend
python src/main.py &

# Start the frontend service
cd /app/frontend
npm start &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $? 